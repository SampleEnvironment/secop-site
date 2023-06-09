Hardware Abstraction
====================


Modules
-------

Definition: Module
    One logical component of an abstract view of the sample environment. Can at least be read.
    May be ’driven' (set new setpoint). May have parameters influencing how it achieves
    its function (e.g. PID parameters). May have some additional diagnostics (read-only) parameters.
    May provide some additional status information (temperature stable?, setpoint reached?)
    Reading a module returns the result of the corresponding physical measurement.

We intentionally avoid the term "device", which might
be misleading, as "device" is often used for an entire apparatus, like a
cryomagnet or humidity cell. In the context of SECoP, an apparatus in
general is composed of several modules. For example different
temperature sensors in one apparatus are to be seen as different modules.

An SEC node controls a set of named modules. Modules also have
some descriptive data (type, list-of-parameters, list-of-commands, ...).

Accessibles
-----------

A module has several accessibles associated with it. An accessible is
addressed by the combination of module and accessible name. Module names
have to be unique within an SEC node, accessible names have to be unique
within a module. There are two basic types of accessibles: parameters and commands.

Module and accessible names should be in English (incl. acronyms), using
only ASCII letters + digits and some additional characters (see section :doc:`protocol`).
The maximum name length is 63 characters.

Parameters
~~~~~~~~~~

Parameter:
    The main parameter of a module is its value. Writable parameters may influence the
    measurement (like PIDs). Additional parameters may give more information about its
    state (running, target reached), or details about its functioning (heater power) for
    diagnostics purposes. Parameters with a predefined meaning are listed in the standard,
    they must always be used in the same way. Custom parameters are defined by the
    implementation of the SEC node, the ECS can use them only in a general way, as their
    meaning is not known.


The following parameters are predefined (this list will be extended):

``"value"``
    represents the *main* value of a module.

.. _BUSY:

``"status"``
    (a tuple of two elements: a status with predefined values
    from an :ref:`enum` as "idle","busy","error", and a describing text).

    .. table:: assignment of status code groups

         ============ ============== =========================================
          statuscode   variant name   Meaning
         ============ ============== =========================================
            0           DISABLED      Module is not enabled
          1XX           IDLE          Module is not performing any action
          2XX           WARN          The same as IDLE, but something may not be alright, though it is not a problem (yet)
          3XX           BUSY          Module is performing some action
          4XX           ERROR         Module is in an error state, something turned out to be a problem.
         ============ ============== =========================================

    .. table:: assignment of sub status (state within the generic state machine)

         ============ ============== =========================================
           subcode     variant name   Meaning
         ============ ============== =========================================
           X0Y         Generic       used for generic modules not having a state machine
           X1Y         Disabling     intermediate state: Standby -> **Disabling** -> Disabled
           X2Y         Initializing  intermediate state: Disabled -> **Initializing** -> Standby
           X3Y         Standby       stable, steady state, needs some preparation steps,
                                     before a target change is effective
           X4Y         Preparing     intermediate state: Standby -> **Preparing** -> Prepared
           X5Y         Prepared      Ready for immediate target change
           X6Y         Starting      Target has changed, but continuous change has not yet started
           X7Y         Ramping       Continuous change, which might be used for measuring
           X8Y         Stabilizing   Continuous change has ended, but target value is not yet reached
           X9Y         Finalizing    Value has reached the target and any leftover cleanup operation
                                     is in progress. If the ECS is waiting for the value of this module
                                     being stable at target, it can continue.
         ============ ============== =========================================

    with ``Y=0`` for now. Future extensions may use different values for Y.

    Since not all combinations are sensible, the following list shows the so far defined codes:

    .. table:: Useful statuscodes

         ====== ================ ========== ============== =========================================
          code   name             generic    variant name   Meaning
         ====== ================ ========== ============== =========================================
             0   DISABLED         DISABLED   Generic        Module is not enabled
           100   IDLE             IDLE       Generic        Module is not performing any action
           130   STANDBY          IDLE       Standby        Stable, steady state, needs some preparation steps,
                                                            before a target change is effective
           150   PREPARED         IDLE       Prepared       Ready for immediate target change
           200   WARN             WARN       Generic        The same as IDLE, but something may not be alright,
                                                            though it is not a problem (yet)
           230   WARN_STANDBY     WARN       Standby        -''-
           250   WARN_PREPARED    WARN       Prepared       -''-
           300   BUSY             BUSY       Generic        Module is performing some action
           310   DISABLING        BUSY       Disabling      Intermediate state: Standby -> **DISABLING** -> Disabled
           320   INITIALIZING     BUSY       Initializing   Intermediate state: Disabled -> **INITIALIZING** -> Standby
           340   PREPARING        BUSY       Preparing      Intermediate state: Standby -> **PREPARING** -> PREPARED
           360   STARTING         BUSY       Starting       Target has changed, but continuous change has not yet started
           370   RAMPING          BUSY       Ramping        Continuous change, which might be used for measuring
           380   STABILIZING      BUSY       Stabilizing    Continuous change has ended, but target value is not
                                                            yet reached
           390   FINALIZING       BUSY       Finalizing     Value has reached the target and any leftover cleanup operation
                                                            is in progress. If the ECS is waiting for the value of this
                                                            module being stable at target, it can continue.
           400   ERROR            ERROR      Generic        An Error occurred, Module is in an error state,
                                                            something turned out to be a problem.
           430   ERROR_STANDBY    ERROR      Standby        An Error occurred, Module is still in Standby state,
                                                            even after ``clear_errors``.
           450   ERROR_PREPARED   ERROR      Prepared       An Error occurred, Module is still in PREPARED state,
                                                            even after ``clear_errors``.
         ====== ================ ========== ============== =========================================

    For the SEC node, it is recommended to use above names (second column) for the status enum type.
    For the ECS, the codes (and not the names) of the status enum are relevant for the meaning.

    The distinction between the status value 360 - 380 is important, if during a target change
    there is a period, where the value changes in a continuous way and measurements might be
    useful. If there is no such period, for example because the value performs some damped oscillation
    from the beginning of the movement, generic BUSY or STABILIZING should be used instead.

    Any undefined status code has to be treated like a generic subcode of the given code number,
    i.e. 376 should be treated as a BUSY_Ramping until it is defined otherwise in the specification.

    .. admonition:: Related Issues

        | :issue:`037 Clarification of status`
        | :issue:`059 set_mode and mode instead of some commands`

    .. note::
        The behavior of a module in each of the predefined states is not yet 100% defined.

    .. note::
        A module only need to declare the status values which it implements. i.e. an Readable module
        does not need a BUSY status.

``"target"``
    present, if the modules main value is to be changeable remotely, i.e. it is at least a Writable

``"pollinterval"``
    a hint to the module for the polling interval in seconds, type is always an double.

``"ramp"``
    (writable parameter, desired ramp. Units: main units/min)

``"setpoint"``
    (ramping setpoint, read only)

``"time_to_target"``
    (read only double, expected time to reach target in seconds)

``"mode"``
    A parameter of datatype enum, for selecting the operation mode of a module.
    The available operation modes can not be predefined in the specification, since
    they depend on the specific module.

    Maximum set of allowed modes:

    .. code:: json

        {"type": "enum", "members": {"DISABLED": 0, "STANDBY": 30, "PREPARED": 50}}

    The meaning of the operation modes SHOULD be described in the description.

    The interplay between the ``mode`` parameter and the status codes can be visualized
    in the following graph:

.. image:: images/status_diagram.svg


Commands
~~~~~~~~

Command:
    Commands are provided to initiate specified actions of the module.
    They should generate an appropriate reply immediately after that action is initiated,
    i.e. should not wait until some other state is reached.
    However, if the command triggers side-effects, they MUST be communicated before the reply is sent.
    Commands may use an possibly structured argument and may return a possibly structured result.
    Commands with a predefined meaning are listed in the standard,
    they must always be used in the same way.

Custom commands are defined by the implementation of the SEC node, the
ECS can use them only in a general way, as their meaning is not known.


The following commands are predefined (extensible):

``"stop"``
     mandatory command on a drivable.
     When a modules target is changed (or, if present, when the ``go`` command is sent),
     it is 'driving' to a new value until the target is reached or until its stop command
     is sent.
     When the ``stop`` command is sent, the SEC node SHOULD set the target parameter
     to a value close to the present one. Then it SHOULD act as if this value would have
     been the initial target.

``"communicate"``
     Used for direct communication with hardware, with proprietary commands. It is useful
     for debugging purposes, or if the implementor wants to give access to parameters not
     supported by the driver. The datatype might be string, or any other datatype suitable
     to the protocol of the device. The ``communicate`` command  is meant to be used in
     module with the ``Communicator`` interface class.

``"reset"``
     optional command for putting the module to a state predefined by the implementation.

``"clear_error"``
     This command tries to clear an error state. It may be called when status is ERROR,
     and the command will try to transform status to IDLE or WARN. If it can not
     do it, the status should not change or change to an other ERROR state before
     returning ``done <module>:clear_errors``

``"go"``
     optional command for starting an action. If the ``go`` command is present,
     changing any parameter (especially the 'target' parameter) does not yet initiate any
     action leading to a BUSY state.
     In contrast, if no 'go' command is present, changing the target will start an action
     trying to change the value to get closer to the target, which usually leads to a BUSY
     state. Changing any parameter, which has an impact on measured values, should
     be executed immediately.

``"hold"``
     optional command on a drivable. Stay more or less where you are, cease
     movement, be ready to continue soon, target value is kept. Continuation can be
     trigger with ``go``, or if not present, by putting the target parameter to its
     present value.

``"shutdown"``
     optional command for shutting down the hardware.
     When this command is sent, and the status is DISABLED,
     it is safe to switch off the related device.

.. note::
    Going to the DISABLED state, may also be triggered by changing the mode to DISABLED.
    If the implementor for security reason wants to prohibit any action after a shutdown,
    this should only be achieved by a shutdown command, as disabling the module should be
    reversible.


Properties
----------

Definition: Properties
    The static information about parameters, modules and SEC nodes is
    constructed from properties with predefined names and meanings.

For a list of pre-defined properties see :ref:`descriptive-data`.

.. _data-report:

Data report
-----------
A JSON array with the value of a parameter as its first element,
and an JSON object containing the qualifiers_ for this value as its second element.

See also: :ref:`data-report`.

.. admonition:: Remark

    Future revisions may append additional elements.
    These are to be ignored for implementations of the current specification

.. _error-report:

Error report
------------
An error report is used in a :ref:`error-reply` indicating that the requested action could
not be performed as request or that other problems occurred.
The error report is a JSON-array containing the name of one of the :ref:`Error
classes <error-classes>`, a human readable string
and as a third element a JSON-object containing extra error information,
which may include the timestamp (as key "t") and possible additional
implementation specific information about the error (stack dump etc.).

See also: `error-report`_.

.. _structure-report:

Structure report
----------------
The structure report is a structured JSON construct describing the structure of the SEC node.
This includes the SEC-node properties, the modules, their module-properties and accessibles
and the properties of the accessibles.
For details see :ref:`descriptive-data`.

.. _value:

Value
-----
Values are transferred as a JSON-Value.

.. admonition:: Programming Hint

    Some JSON libraries do not allow all JSON values in their (de-)serialization functions.
    Whether or not a JSON value is a valid JSON text, is controversial,
    see this `stackoverflow issue <https://stackoverflow.com/questions/19569221>`_
    and :rfc:`8259`.

    (clarification: a *JSON document* is either a *JSON object* or a *JSON array*,
    a *JSON value* is any of a *JSON object*, *JSON array*, *JSON number* or *JSON string*.)

    If an implementation uses a library, which can not (de-)serialize all JSON values,
    the implementation can add angular brackets around a JSON value, decode it
    and take the first element of the result. When encoding the reverse action might be
    used as a workaround. See also :RFC:`7493`


.. _qualifiers:

Qualifiers
----------

Qualifiers optionally augment the value in a reply from the SEC node,
and present variable information about that parameter.
They are collected as named values in a JSON-object.

Currently 2 qualifiers are defined:

``"t"``
    The timestamp when the parameter has changed or was verified/measured (when no timestamp
    is given, the ECS may use the arrival time of the update message as the timestamp).
    It SHOULD be given, if the SEC node has a synchronized time,
    the format is that of a UNIX time stamp, i.e. seconds since 1970-01-01T00:00:00+00:00Z,
    represented as a number, in general a floating point when the resolution
    is better than 1 second.

    .. note::
        To check if a SEC node supports time stamping, a `ping` request can be sent.
        (See also :ref:`heartbeat`).

``"e"``
   the uncertainty of the quantity. MUST be in the same units
   as the value. So far the interpretation of "e" is not fixed.
   (sigma vs. RMS difference vs. ....)

other qualifiers might be added later to the standard.
If an unknown element is encountered, it is to be ignored.


.. _interface-classes:

Interface Classes
-----------------

The idea is, that the ECS can determine the functionality of a module
from its class.

The standard contains a list of classes, and a specification of the
functionality for each of them. The list might be extended over time.
Already specified base classes may be extended in later releases of the
specification, but earlier definitions will stay intact, i.e. no
removals or redefinitions will occur.

The module class is in fact a list of classes (highest level class
first) and is stored in the module-property `interface_classes`.
The ECS chooses the first class from the list which is known to it.
The last one in the list must be one of the base classes listed below.

.. admonition:: Remark

    The list may also be empty, indicating that the module in question does
    not even conform to the Readable class!

Base classes
~~~~~~~~~~~~

``"Communicator"``
    The main purpose of the module is communication.
    It may have none of the predefined parameters of the other classes.

    The ``communicate`` command is used mainly for debugging reasons, or as a workaround
    for using hardware features not implemented in the SEC node.

.. _Readable:

``"Readable"``
    The main purpose is to represent readable values (i.e. from a Sensor).
    It has at least a ``value`` and a ``status`` parameter.

.. _Writable:

``"Writable"``
    The main purpose is to represent fast settable values (i.e. a switch).
    It must have a ``target`` parameter in addition to what a `Readable`_ has.

.. _Drivable:

``"Drivable"``
    The main purpose is to represent slow settable values (i.e. a temperature or a motorized needle valve).
    It must have a ``stop`` command in addition to what a `Writable`_ has.
    Also, the ``status`` parameter will indicate a `BUSY`_ state for a longer-lasting operations.
