Using the ``check`` message for dry-run validation
===================================================

.. note::

   This guide is based on the SECoP protocol specification published by
   the International Society for Sample Environment (ISSE), available at
   https://github.com/SampleEnvironment/SECoP and
   https://sampleenvironment.github.io/secop-site/specification/index.html.
   It assumes you are already comfortable with the basic SECoP request/reply
   cycle and with the `change` message in particular.  If you are not, the
   :doc:`companion guide on the SECoP busy sequence <busy-sequence>` is a good starting point.

Introduction
------------

Before actually moving a magnet to a new field, or commanding a motor to a new
position, it would be useful to ask the instrument: *"would this value even work
right now?"* without committing to the action.

SECoP provides exactly this capability through the optional ``check`` message.
``check`` is a dry-run mechanism: the ECS asks the SEC node to validate a
value without applying it.  The SEC node inspects the request just as it would
for a real ``change`` or ``do``, and replies either ``checked`` (the value
would be accepted) or ``error_check`` (it would be refused, with a reason).
Nothing on the hardware, and nothing in the SEC node's parameter state, is
touched in the process.

Because ``check`` is optional, a SEC node that does not implement it will reply
with a ``ProtocolError``.  An ECS should therefore treat a ``ProtocolError``
reply to a ``check`` request as "dry-run is not available on this node," and
fall back to ordinary ``change``/``do`` messages if it still wants to proceed.

Why is dry-run validation useful?
----------------------------------

The most common reason to use ``check`` is to give immediate, informative
feedback to a user or to an automated script, *before* anything is
physically started.

Consider a vector magnet with three independent coil axes.  The accessible
value for the field target is a three-component list.  Not every combination
of field components is technically reachable: the combined magnitude may be
limited, or certain directions may be mechanically or thermally restricted
given the current cryostat configuration.  These constraints are too complex to
encode fully in the accessible's :ref:`datainfo <data-types>`: ``datainfo`` can
express a simple scalar range, but not an arbitrary constraint surface.

Without ``check``, the ECS can only find out whether a value is acceptable by
actually sending a ``change`` message.  If the value is wrong, the SEC node
will refuse it and nothing changes, but the ECS may already have changed its
internal state, updated its GUI, and written to a log.  With ``check``, the
ECS can ask first, present the user with a clear error message, and not take
any further action until the user provides a valid value.

A second important use case is *scripted experiment automation*.  An automated
scan script may calculate a list of setpoints ahead of time.  Running ``check``
on every setpoint at the start of the script catches values outside the allowed
range before the scan begins, rather than failing partway through a long
overnight measurement.

The ``check`` Message Format
----------------------------

The ``check`` message follows the same wire format as ``change``: an action
word, a ``<module>:<accessible>`` specifier, and a JSON value.  The normative
definition of all three messages in this family is in
:doc:`/specification/messages/optional`.

A ``check`` request produces exactly one of three direct replies:

* ``checked``: the value would be accepted.
* ``error_check``: the value would be refused (with a reason).
* ``error_check`` with error class ``ProtocolError``: the SEC node does not
  implement ``check`` at all.

The sub-sections below cover each case.

``check``
~~~~~~~~~

The initial ``check`` request::

    > check <module>:<accessible> [<value>]

The specifier is the name of a module and one of its accessibles, separated by
a colon, exactly the same syntax as for a `change` or `do` message.  The
data part is the value to be validated.

``checked`` and ``error_check``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the validation succeeds, the SEC node replies with::

    < checked <module>:<accessible> <data-report>

The :ref:`data report <data-report>` in a ``checked`` reply contains the validated value (the
same value as sent in the request, possibly normalised by the SEC node).

If the validation fails, the reply is::

    < error_check <module>:<accessible> <error-report>

The :ref:`error report <error-report>` is a three-element JSON array of the form
``["<ErrorClass>", "<human-readable message>", {<optional extra info>}]``.
The ``ErrorClass`` tells the ECS *why* the value was rejected:

* `RangeError` means the value falls outside the limits encoded in the
  accessible's :ref:`datainfo <data-types>`.  This error does not depend on the current state
  of the SEC node; the same value would always be rejected.
* `Impossible` means the value is technically within the datainfo limits,
  but the current configuration of the SEC node makes it unreachable right now
  (for example, a vector field target that is outside the reachable sphere
  given the current cryostat temperature).  The same value might be accepted
  later if the conditions change.
* `NotCheckable` means the accessible does not support dry-run validation
  because its `checkable` property is absent or ``false``.

Important constraints
---------------------

The ``check`` message comes with two guarantees that distinguish it from a real
``change`` message:

1. **A** ``check`` **message must not change anything.**
   Neither the hardware state nor any SEC node parameter is modified.  The SEC
   node is only *reading* its current state to evaluate the request; it does
   not act on it.  An ECS can therefore send ``check`` at any time, even while
   the module is busy, without risking interference with an ongoing action.

2. **The response to a** ``check`` **must not depend on the module's status.**
   Whatever the module's :ref:`status <status-codes>` (IDLE, BUSY, ERROR), the ``check``
   reply for any given value must always be the same.  The ``check`` message
   evaluates the value against the node's *configuration* (physical limits,
   interlocks, geometry constraints), not against its *current activity*.

A third important difference from `update` events: the ``checked`` and
``error_check`` replies are sent **only to the client that sent the ``check``
request**.  They are not broadcast to other connected clients.

The ``checkable`` property
--------------------------

The :ref:`accessible description <accessible-description>` in a ``describe`` reply may carry a boolean property
`checkable`.  When present and ``true``, the accessible can be validated with
``check``.  When absent or ``false``, the SEC node will reply with a
`NotCheckable` error.

.. code-block:: json

    "target": {
        "description": "target field vector",
        "datainfo": {
            "type": "array",
            "minlen": 3,
            "maxlen": 3,
            "members": {"type": "double", "unit": "T"}
        },
        "readonly": false,
        "checkable": true
    }

An ECS that wants to offer dry-run feedback to users should read the
``checkable`` flag from the description and only show or enable the
"Check value" feature for those accessibles where it is supported.

Examples
--------

Example 1: a valid field target
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ECS asks whether the vector field ``[1.0, 1.0, 2.0]`` is reachable on a
magnet module ``mf``.  The SEC node determines that the value is inside its
allowed sphere and confirms it::

    > check mf:target [1.0, 1.0, 2.0]
    < checked mf:target [[1.0, 1.0, 2.0], {}]

The ``checked`` reply contains the value wrapped in the standard data-report
format (``[<value>, <qualifiers>]``).

Example 2: a value outside the reachable sphere
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ECS asks about ``[1.0, 2.0, 2.5]``, which lies just outside the allowed
field sphere for the current cryostat configuration::

    > check mf:target [1.0, 2.0, 2.5]
    < error_check mf:target ["BadValue", "value outside allowed sphere", {"closest_valid": [0.8, 1.6, 2.0]}]

The SEC node rejects the value.  Note that the error report's third element
carries additional context (``"closest_valid"``) that the ECS or the user can
inspect to understand what value *would* have been accepted.

Example 3: an accessible that does not support ``check``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some accessibles simply cannot be pre-validated, for example a parameter
whose acceptance depends entirely on transient hardware state.  If an ECS tries
to ``check`` such an accessible, the SEC node replies::

    > check cryo:target 2.7
    < error_check cryo:target ["NotCheckable", "", {}]

This is not a protocol error; it just means that dry-run validation is not
available for this particular accessible.  The ECS should fall back to a direct
``change`` if it still wants to set the value.

Example 4: a ``check`` on an unsupported SEC node
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the SEC node does not implement ``check`` at all, it replies with a
`ProtocolError`::

    > check t1:target 300
    < error_check t1:target ["ProtocolError", "check is not supported", {}]

An ECS should interpret this as a permanent signal that dry-run validation is
unavailable on this node and disable any related UI elements for the duration
of the connection.

Putting it together: a validation workflow
------------------------------------------

A typical ECS workflow that uses ``check`` before committing to a ``change``
might look like this::

    # User has entered a new target of [1.0, 1.0, 2.0] in the GUI.

    > check mf:target [1.0, 1.0, 2.0]
    < checked mf:target [[1.0, 1.0, 2.0], {}]

    # Validation passed. Now send the real change request.
    > change mf:target [1.0, 1.0, 2.0]
    < update mf:status [[300, "ramping field"], {...}]
    < update mf:target [[1.0, 1.0, 2.0], {...}]
    < changed mf:target [[1.0, 1.0, 2.0], {...}]

Compared to calling ``change`` directly, the cost of the extra round-trip is
usually negligible.  The benefit of catching configuration-level errors before
touching the hardware can be significant, particularly for complex or slow
instruments.

Note that the ECS should not rely on the result of a ``check`` remaining valid
forever.  Between the ``checked`` reply and the subsequent ``change``, the SEC
node's configuration could change (a safety interlock could trip, another
client could move a coupled module, etc.).  The ``check`` message is a
point-in-time assessment, not a reservation.

Summary
-------

* The ``check`` message allows an ECS to validate a value against a SEC node's
  current configuration without actually changing anything.  It is a dry run
  for ``change`` and ``do``.
* The SEC node replies with ``checked`` (validation passed) or ``error_check``
  (validation failed, with a reason).
* A ``check`` must never modify hardware or parameters, and its result must not
  depend on the module's current ``status``.
* The accessible property ``checkable: true`` indicates that an accessible
  supports the ``check`` message.
* Replies to ``check`` are sent only to the requesting client, not broadcast.
* ``check`` is optional.  A ``ProtocolError`` reply means the SEC node does not
  implement it; a ``NotCheckable`` error means this particular accessible cannot
  be pre-validated.
* Use ``check`` to give users early feedback, to validate automated setpoints
  before a scan, and to make complex, configuration-dependent constraints
  visible to the ECS without incurring any side effects.

Further reading
---------------

* :doc:`/specification/messages/optional`
* `checkable`: accessible property enabling dry-run support
* :doc:`/specification/messages/readwrite`
* :doc:`/specification/messages/commands`
* :ref:`error-reply`
* :ref:`data-types`
* :issue:`075 New messages check and checked`
