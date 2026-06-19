Coupled Modules - Understanding SECoP Inter-Module Interactions
===============================================================


.. note::

   This tutorial is based on the SECoP protocol specification published by
   the International Society for Sample Environment (ISSE), available at
   https://github.com/SampleEnvironment/SECoP and
   https://sampleenvironment.github.io/secop-site/specification/index.html.
   It focuses on a single concept: how SECoP describes *coupling* between
   two modules that compete for, or hand off, control of a piece of
   hardware, expressed through the ``controlled_by`` and
   ``control_active`` parameters. This tutorial assumes familiarity with
   the SECoP handshake (``change``/``do``, ``update``, and the ``status``
   parameter), as described in the companion tutorial on that topic.

Introduction
------------

So far we have treated SECoP modules as if each one independently owned
its own little piece of hardware: a module has a ``value``, maybe a
``target``, and a ``status`` that tells the ECS whether it is busy. In
practice, sample environment hardware is rarely that tidy. A single
physical device often exposes *several* SECoP modules that are not
independent at all, because underneath they share the same actuator.

Two classic examples:

* A temperature controller drives a heater. The ECS may see two
  modules: a temperature module ``T`` (a *Drivable*, with a target
  temperature) and a heater-power module ``heaterpower`` (a
  *Writable*, with a target power in Watts). Normally ``T``
  decides how much power to apply -- but a user doing instrument
  commissioning might want to bypass the control loop and set the
  heater power directly.
* A power supply for a magnet can be operated in constant-current mode
  or constant-voltage mode, but never both at once. The ECS sees two
  modules, ``I`` and ``V``, each independently writable -- yet writing
  to one must implicitly disable the other.

SECoP needs a standard way to describe "these two modules share an
actuator, and right now, *this* one is the one actually steering it."
That is exactly what ``controlled_by`` and ``control_active`` are for.

Why is this needed at all?
--------------------------

Without an explicit coupling mechanism, the situations above would be
invisible to the ECS, with consequences that range from confusing to
dangerous:

* **Silent loss of control.** If the ECS sets ``heaterpower:target`` to
  some fixed value to do a manual measurement, and the temperature
  module ``T`` is still internally running its control loop, ``T`` may
  overwrite that value moments later. The ECS would have no way of
  knowing why its setting "didn't stick."
* **Two writers, one wire.** With the ``I``/``V`` power supply, nothing
  in a plain SECoP module description prevents an ECS (or a confused
  user) from writing to both ``I:target`` and ``V:target`` in the same
  session. Without a coupling indicator, the ECS cannot tell that doing
  so is contradictory, nor which of the two settings is actually in
  effect.
* **No way to ask "who is in charge right now?"** Even if the firmware
  internally handles the conflict sensibly, the ECS -- and the human
  using it -- still need a parameter to *read*, to decide whether it is
  safe or sensible to issue a particular command at this moment.
* **No standard way to hand over control.** Switching from automatic to
  manual heater control (and back) needs a defined trigger and a
  defined, observable outcome, in the same self-describing spirit as
  the rest of SECoP. It should not require a custom, undocumented
  parameter every single instrument re-invents.

SECoP's answer is two read-only parameters, present on the modules
that participate in the coupling, plus an ordinary ``target``/``go``
write to switch which module is in control -- following the very same
handshake rules already familiar from ``change`` and ``do``.

The two parameters involved
---------------------------

``controlled_by`` -- "who is driving me?"
    A read-only parameter of datatype ``enum``, whose possible values
    are the names of other modules, plus the special value ``"self"``
    (which must be enum value ``0``). A module that has this parameter
    is declaring: "my behaviour may currently be dictated by one of
    these other named modules, instead of by my own ``target``."

``control_active`` -- "am I the one actually in control?"
    A read-only boolean on a *Drivable* or *Writable*
    module. When ``true``, the module's own control mechanism is
    trying to bring its ``value`` to its ``target`` -- this is the
    normal, "business as usual" case, and is also the implicit default
    for a module that does not even have this parameter. When
    ``false``, that control mechanism is switched off and the module's
    own ``target`` is *not* considered any more; the module behaves
    like a plain *Readable* until control is handed back to it.

These two parameters are normally used together, on a *pair* of
coupled modules, to describe the two sides of the same coin.

Case 1: a controller and a controlled actuator
-----------------------------------------------

This is the temperature/heater example. Module ``T`` (temperature) can
control module ``heaterpower`` (heater power). They are never both
"in charge" of the heater at the same time.

.. list-table::
   :header-rows: 1
   :widths: 25 30 45

   * - State
     - Module ``T``
     - Module ``heaterpower``
   * - T is controlling
     - ``control_active=true``
     - ``controlled_by="T"``, ``control_active=false``
   * - heaterpower is self-controlled
     - ``control_active=false`` [1]_
     - ``controlled_by="self"``, ``control_active=true``

.. [1] When ``T`` is not controlling, it has no ``heaterpower`` to act
   through, so reaching its own ``target`` is simply not happening;
   reading ``T:status`` will typically reflect this.

How control is taken
~~~~~~~~~~~~~~~~~~~~~

The rule given by the specification is simple and symmetric: **whichever
module receives a target change (or a** ``go`` **command, if present)
takes over control.**

* Writing ``change T:target ...`` (or sending ``go`` to ``T``) makes
  ``T`` take over control. Before the SEC node sends back the
  ``changed``/``done`` reply for that request, it must already have set
  ``heaterpower:controlled_by`` to ``"T"`` and updated both modules'
  ``control_active`` parameters correctly.
* Writing ``change heaterpower:target ...`` makes ``heaterpower`` take
  back control for itself. The SEC node must set
  ``heaterpower:controlled_by`` to ``"self"`` and again update both
  ``control_active`` parameters before replying.

This "update side effects before replying" rule should look familiar:
it is exactly the same rule used in the handshake tutorial for
``status`` changes. Here, ``controlled_by`` and ``control_active`` are
simply two more parameters that count as "side effects" of a target
change, and must be communicated -- via ``update`` events to all
activated clients -- before the direct reply is sent.

Explicitly releasing control: ``control_off``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Setting a module's ``target`` always turns its own control back *on*.
But what if there is no controlling module to hand off to -- for
instance, a temperature loop with no heater module exposed at all, or
one where the heater happens not to be a *Writable*? For this
case, a module may offer the optional ``control_off`` command, whose
only job is to set ``control_active`` to ``false`` directly. More
generally, ``control_off`` can be thought of as putting the module into
an "energy saving" state: switching off active heating/cooling for a
temperature loop, or cutting drive current for a motor.

.. image:: /_static/controlled_by_controller_coupling_en.svg
   :alt: Diagram of module T and heaterpower switching control via controlled_by and control_active
   :width: 100%

A worked example
~~~~~~~~~~~~~~~~~

Both connections below have already sent ``activate``; qualifiers are
abbreviated as ``{...}``::

    > read T:control_active
    < reply T:control_active [true,{...}]
    > read heaterpower:controlled_by
    < reply heaterpower:controlled_by ["T",{...}]

    > change heaterpower:target 5.5
    < update heaterpower:controlled_by ["self",{...}]
    < update T:control_active [false,{...}]
    < update heaterpower:control_active [true,{...}]
    < update heaterpower:target [5.5,{...}]
    < changed heaterpower:target [5.5,{...}]

A user has just taken manual control of the heater to run it at a fixed
5.5 W, bypassing ``T``'s control loop. Notice the order: the coupling
parameters (``controlled_by``, both ``control_active`` flags) are
announced as ``update`` events *first*; only then does the ``target``
update and the final ``changed`` reply follow -- precisely the
side-effects-before-reply ordering from the handshake.

Handing control back is the mirror image::

    > change T:target 300
    < update heaterpower:controlled_by ["T",{...}]
    < update T:control_active [true,{...}]
    < update heaterpower:control_active [false,{...}]
    < update T:target [300,{...}]
    < update T:status [[300,"ramping"],{...}]
    < changed T:target [300,{...}]

Setting a new target on ``T`` reclaims control of the heater for the
control loop, and -- exactly as in an ordinary single-module
handshake -- ``T`` may now also go ``BUSY`` while it ramps towards 300 K.
The two concepts compose cleanly: coupling decides *who* is allowed to
drive the hardware right now, while ``status`` (as covered in the
handshake tutorial) describes whether *that* module is currently busy
doing so.

Case 2: two mutually exclusive writable modules
------------------------------------------------

The second pattern in the specification has no single "controller"
module; instead, two peer modules, ``I`` (current) and ``V`` (voltage)
on a power supply, are mutually exclusive alternatives. Exactly one of
them is ever ``controlled_by="self"`` at a time.

.. list-table::
   :header-rows: 1
   :widths: 25 37 38

   * - State
     - Module ``I``
     - Module ``V``
   * - constant current
     - ``controlled_by="self"``, ``control_active=true``
     - ``controlled_by="I"``, ``control_active=false``
   * - constant voltage
     - ``controlled_by="V"``, ``control_active=false``
     - ``controlled_by="self"``, ``control_active=true``

.. image:: /_static/controlled_by_iv_coupling_en.svg
   :alt: Diagram of module I and V toggling between constant current and constant voltage via controlled_by and control_active
   :width: 100%

The module with ``control_active=false`` behaves like a plain
*Readable*: its own ``target`` is ignored entirely, even though
the parameter is still present and (for the inactive module) simply
not taken into account. Writing to the *other* module's ``target`` is
what flips the supply from one mode to the other, toggling both
modules' ``control_active`` flags as a side effect::

    > read I:control_active
    < reply I:control_active [true,{...}]
    > read V:control_active
    < reply V:control_active [false,{...}]

    > change V:target 12
    < update I:controlled_by ["V",{...}]
    < update I:control_active [false,{...}]
    < update V:controlled_by ["self",{...}]
    < update V:control_active [true,{...}]
    < update V:target [12,{...}]
    < changed V:target [12,{...}]

After this exchange, the power supply is now in constant-voltage mode
at 12 V; any value still present in ``I:target`` is simply not acted
upon until ``I`` is given a new target of its own.

What if more than two modules share one controller?
----------------------------------------------------

The specification notes that a single controlling module may need to
arbitrate between *several* controlled modules at once -- for example,
a liquid-helium cryostat's temperature controller might, in turn,
control both a heater-power module and a helium-flow/pressure module
for cooling. In such cases, ``controlled_by`` and ``control_active``
alone are not expressive enough to choose *which* secondary mode is
active; the specification allows additional, implementation-specific
parameters for that finer-grained selection (the example given is a
custom parameter such as ``_automatic_nv_pressure_mode``). The
takeaway for the ECS author is: ``controlled_by``/``control_active``
reliably answer "is this module currently steering its own hardware,
or not?", but on more complex instruments there may be additional,
device-specific parameters layered on top to describe richer
arbitration logic.

Why this fits the rest of SECoP's design
-----------------------------------------

It is worth noting what SECoP does *not* introduce here: there is no
new message type, no new handshake step, and no special "take control"
command in the general case (only the optional ``control_off`` adds a
new command, and only where there is no module to hand control back
to). Coupling is expressed entirely through:

* two ordinary, read-only parameters (``controlled_by``,
  ``control_active``) that any generic SECoP client already knows how
  to read, poll, or subscribe to via ``activate``, and
* the existing ``change``/``go`` handshake, whose "side effects before
  reply" rule is simply asked to also cover these two parameters
  whenever a target change causes a hand-over of control.

This is consistent with SECoP's general design philosophy: rather than
inventing protocol-level machinery for every new situation, new
semantics are expressed as additional, self-describing parameters
layered on top of the same small set of messages introduced for the
basic handshake.

Summary
-------

* Two (or more) SECoP modules can share a single physical actuator.
  SECoP makes this explicit via the read-only parameters
  ``controlled_by`` (which module currently has control, or
  ``"self"``) and ``control_active`` (whether *this* module's own
  control loop is currently engaged).
* Control is taken implicitly: whichever module receives a ``target``
  change (or ``go`` command) becomes the one in control, and the SEC
  node updates ``controlled_by``/``control_active`` on both modules
  accordingly.
* A module without an alternative to hand control to may offer the
  optional ``control_off`` command, simply switching its own
  ``control_active`` to ``false``.
* These coupling updates must be communicated to all activated clients
  *before* the direct reply to the triggering ``change``/``do``
  request -- exactly the same side-effects-before-reply rule already
  used for ``status`` transitions in the basic handshake.
* For more complex arbitration between several controlled modules,
  instruments may add further custom, device-specific parameters on
  top of this basic mechanism.

Further reading
---------------

* `4.5. Parameters and commands -- Coupled modules
  <https://sampleenvironment.github.io/secop-site/specification/accessibles.html#coupled-modules>`_
* `4.4. Interface classes (Readable, Writable, Drivable)
  <https://sampleenvironment.github.io/secop-site/specification/classes.html>`_
* `read, change: Read and write parameters
  <https://sampleenvironment.github.io/secop-site/specification/messages/readwrite.html>`_
* `SECoP Issue 059: set_mode and mode instead of some commands
  <https://github.com/SampleEnvironment/SECoP/blob/master/issues/059%20set_mode%20and%20mode%20instead%20of%20some%20commands.rst>`_
