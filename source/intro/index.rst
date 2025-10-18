============
Introduction
============

.. TODO add diagrams!

This section will give an overview over the different parts of SECoP described
in the different chapters of :doc:`the specification </specification/index>`.

We will start with the structural concept for the SECoP server, move on to the
messages and in the end learn what the description is for a SECoP server and
which datatypes are supported.

Background
----------

SECoP developed out of the need of multiple large scale facilities in the
neutron science world to make equipment easier to share between facilities.
This should not deter you from using it, as its flexibility allows for a wide
range of use cases.

.. metadata, why not x?, semantics, not just syntax, sine2020/hmc, machine/human readable
   talk slide 7
   philosophy talk slide 16
   word doc


SECoP Node Structure
--------------------

- SECoP is a communication protocol with a client-server model.  The server is
  called the "SEC node".

- Each SEC node consists of one or more "modules".  These represent the main
  interface for interacting with the hardware.

- Each of these modules can have static values which are known at startup and
  dynamic values.  These are called "properties" and :doc:`parameters
  </specification/accessibles>` respectively.  Parameters can in turn have their
  own properties.

  Examples of properties would be the datatype of the parameter or the
  `readonly` flag that shows whether a parameter may be written to or not.

  To initiate actions that may not necessarily be tied to a parameter, modules
  can also have :doc:`commands </specification/accessibles>`, like stopping the
  current movement or running a calibration.

- To show which capabilities a module supports, and to give a name to common
  groupings, there are :ref:`interface-classes` and :ref:`features`.

  The most important interface classes are `Readable`, `Writable` and
  `Drivable`.

- Readable modules have a ``value`` and a ``status`` parameters, which show the
  current error state of the module.  As the name implies, the main value can
  only be read.

- Writable and Drivable modules allow influencing their value by writing to a
  ``target`` parameter.  Writables are intended for fast operations like
  switches, where the target state can be reached quickly (i.e. sub-second
  operations or similar).  Drivables funcion similar, but they can take longer
  to reach the target state.  Think of a motor that has to drive to a position
  along a rail.  For this, they would reflect the ongoing operation in their
  status, setting it to ``BUSY`` and returning to ``IDLE`` once the operation is
  complete.


Description
-----------

The description is a formalized structure containing all information about the
SEC node's modules and their properties, parameters and commands.  It is machine
readable, with all details about modules, parameters, datatypes and so on
included.  Additionally, the implementor of the SEC node has to include textual
descriptions for the important parts of the SEC node.  These short documentation
texts are not intended for machines, but for the human operators of the
equipment.  Functional dependencies that have to be machine readable are exposed
through the already mentioned :ref:`interface-classes` and :ref:`features`.

For the representation details, see the section :ref:`descriptive-data`.


Data types
----------

A variety of datatypes are covered in SECoP.  There are simple datatypes, for
example:

- :ref:`Integer <int>`
- :ref:`Scaled Integer <scaled>`
- :ref:`Floating Point <double>`
- :ref:`Boolean <bool>`
- :ref:`Enum <enum>`
- :ref:`String <string>`
- :ref:`Blob <blob>`
- :ref:`Matrix <matrix>`

For more complicated values, there are three structured datatypes:

- :ref:`Array <array>`, an array of uniform values
- :ref:`Tuple <tuple>`, a fixed sequence of items that can be of different types
- :ref:`Struct <struct>`, a collection of named members, each of which has its
  own type


Implementations
---------------

Implementing SEC nodes is best done with one of the preexisting frameworks.

Depending on your background or the technologies already in use with your
facility, you can choose the :doc:`implemenation <../implementations/index>`
that suits your needs best.


Communication protocol
----------------------

If you prefer to implement SECoP from ground up, this section gives the basics
about the protocol.

SECoP is a line-based protocol.  The communication between client and server
builds upon :doc:`messages </specification/messages>` which are transferred
between SEC node and client.

Examples of messages are::

    describe
    read temp:setpoint
    change temp:target 15.0
    update temp:value [15.3, {"t": 1736239123.0}]

There are three parts a message can have: ``action``, ``specifier`` and
``data``. Of these, depending on the action, ``specifier`` and ``data`` may not
be needed.

- The first part, ``action``, specifies the kind of message we want to send.
- The middle part, ``specifier``, points to the module, parameter or command we
  want to operate on.
- Finally, ``data`` is the JSON-formatted data that may be needed for the
  specified action, like the new value when writing to a parameter, or the
  argument of a command.

The default mode for communicating between SEC node and client is a classic
request-response mode, where the client initiates an exchange.  However, if the
SEC node implementation supports it, the client may choose to move to the
asynchronous mode, where the SEC node will send updates asynchronously when they
occur.  For more details on this, see the `activate` message.

..
    Problems:

    Different Instrument Control Softwares with different ways to control SE
    Complex SE software interface protocols (Taco/Tango, EPICS…)
    Time consuming integration of new or external SE equipment (no easy mobility)

    No standard for SE metadata

    "…a common standard protocol for interfacing sample environment equipment to instrument control software.
    …compatible with a broad variety of soft- and hardware operated at the different LSF’s…
    …The adoption of this standard will greatly facilitate the installation of new equipment and the sharing of equipment between the facilities…
    …Implementations of the Sample Environment Communication Standard Protocol (SECoP) will then be tested at different facilities and provided to interested industrial partners for implementation…
    …In the context of SECoSP all sample environment related metadata has to be made available in a standard form
    Simple: all parts of SECoP (transport layer, syntax) should be as simple as possible (but as complex as needed).
    Inclusive: enable the use of SECoP by ECSs with a great variety of design concepts (e.g. synchronous vs. asynchronous communication).
    Self-explaining: the description of a SEC node must contain all necessary information for a) operating the SEC node by the ECS without further documentation in at least a basic mode, b) providing all relevant metadata information.
    Definitions: Necessary - sufficient – unambiguous, don’t define what does not have to be defined.
    Transport layer: byte oriented (TCP/IP, serial), ASCII
    Protocol is independent from specific transport layer.
    Complex functionality of the sample environment equipment (on the SEC-node side) is wrapped so that a simplified and standardized use of SE equipment by the ECS is possible.
    Basic SECoP plug-and-play operation must always be possible.
    Keep the overhead for the SECoP protocol on SEC node (server) side small.
    Avoid unnecessary traffic.
    Better to be explicit.
    All protocol messages must be human readable (with only exception: blob).
    Names in SECoP are treated as case sensitive but must be unique if lowercased.
    Use JSON.
    Impose best-practices to the programmer of the SEC node by making important features mandatory.
    Must ignore policy
    Allow for multiple clients.
    If multiple clients are connected to a SEC-node, only one of them should change parameters or send commands. Otherwise resulting problems might not be handled by SECoP.
    There should be a general way of doing things.
    why not mqtt etc.
    machine+human
