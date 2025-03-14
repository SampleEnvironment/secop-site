=================================
Getting to know the bare protocol
=================================

Here we want to show you how to get started with SECoP.  We will begin by having
a look on how to manually interact with a running SEC node.  In the end, you
probably won't be using it this way, instead choosing a client which handles a
lot of the logic for you.  Nevertheless, understanding what happens on the wire
may be beneficial, so read on if you want to, or skip over to the sections about
the clients.

.. TODO: links to sections!

~~~~~~~~~~~~~~~~~~~~~
Talking to a SEC node
~~~~~~~~~~~~~~~~~~~~~

So you have never used SECoP, and want to interact with a node?  For exploring
the protocol, all you need is a program that can talk tcp or serial, depending
on your device.  Connect to your device and send the :ref:`identification
message <message-identification>` ``*IDN?`` to start communication ('>' and '<'
show who is sending the message):

.. code::

    > *IDN?

The SEC node replies with the version number of the protocol that it wants to
speak:

.. code::

    < ISSE,SECoP,V2019-09-16,v1.0

Great!  So we know that we are talking to something that knows SECoP, but we do
not know yet what we are talking to.  That is what we will find out with next
message.


~~~~~~~~~~~~~~~
The Description
~~~~~~~~~~~~~~~

.. code::

    > describe

We will format the answer a bit, since it is longer than the usual messages we
will encounter.  We will step through it afterwards.

.. dropdown:: Click to show the whole description

  .. code::

    < describing . {
        "equipment_id": "example_heater",
        "description": "a basic example temperature SEC node.",
        "firmware": "ExampleSECoPFirmware",
        "modules": {
          "outside": {
            "interface_classes": ["Readable"],
            "description": "Outside temperature monitor.",
            "features": [],
            "implementation": "example.sensors.Temperature",
            "accessibles": {
              "value": {
                "description": "current value of the module",
                "datainfo": {
                  "type": "double",
                  "unit": "°C"
                },
                "description": "temperature outside",
                "readonly": true
              },
              "status": {
                "description": "current status of the module",
                "datainfo": {
                  "type": "tuple",
                  "members": [
                    {
                      "type": "enum",
                      "members": {
                        "IDLE": 100,
                        "WARN": 200,
                        "ERROR": 400
                      }
                    },
                    { "type": "string" }
                  ]
                },
                "readonly": true
              }
            }
          },
          "heater": {
            "description": "Example Heater",
            "implementation": "example.actuators.Heater",
            "interface_classes": ["Drivable"],
            "features": []
            "accessibles": {
              "value": {
                "description": "current value of the module",
                "datainfo": {
                  "type": "double",
                  "unit": "°C"
                },
                "readonly": true
              },
              "status": {
                "description": "current status of the module",
                "datainfo": {
                  "type": "tuple",
                  "members": [
                    {
                      "type": "enum",
                      "members": {
                        "IDLE": 100,
                        "WARN": 200,
                        "BUSY": 300,
                        "ERROR": 400
                      }
                    },
                    {
                      "type": "string"
                    }
                  ]
                },
                "readonly": true
              },
              "target": {
                "description": "target value of the module",
                "datainfo": {
                  "unit": "°C",
                  "type": "double"
                },
                "readonly": false
              },
              "stop": {
                "description": "Stop heating, stay at current temperature.",
                "datainfo": {
                  "type": "command"
                }
              },
              "_maxheaterpower": {
                "description": "maximum allowed heater power",
                "datainfo": {
                  "unit": "W",
                  "min": 0.0,
                  "max": 100.0,
                  "type": "double"
                },
                "readonly": false
              },
              "_examplecommand": {
                "description": "Do some calculation.",
                "datainfo": {
                  "type": "command",
                  "argument": {
                    "type": "struct",
                    "members": {
                      "a": {
                        "min": 0.0,
                        "max": 10.0,
                        "type": "double"
                      },
                      "b": {
                        "type": "double"
                      }
                    }
                  },
                  "result": {
                    "type": "double"
                  }
                }
              }
            },
          }
        }
      }


SEC node information
^^^^^^^^^^^^^^^^^^^^

.. code::

    < describing . {
        "equipment_id": "example_org.example_heater",
        "description": "a basic example temperature SEC node.",
        "firmware": "ExampleSECoPFirmware v0.5",

The first few elements here are describing the capabilities of the SEC node
itself.  They include the firmware and version, the exposed interfaces and the
unique equipment ID.  The description is intended for humans to read.  It can be
longer than the short example here, and in the best case should include
information that is useful for the operator, like the most important modules,
usage hints or whatever else could be needed by a human operator beyond the
information that SECoP provides.

The next element contains all modules available on the SEC node: in this case
``outside`` and ``heater``.


Module information
^^^^^^^^^^^^^^^^^^

.. code::

    "modules": { "outside": { ... }, "heater": { ... } }

We will fist have a look at the smaller ``outside`` module:

.. code:: json

    "implementation": "example.sensors.Temperature",
    "description": "Outside temperature monitor.",
    "interface_classes": ["Readable"],
    "features": [],

The ``implementation`` string is not standardized, but gives a hint where to
find the implementation for this Module for debugging purposes, e.g. the class
or source file where this module is defined.  The ``interface_classes`` tells
the client which capabilities the module supports.  In this case, it is a
``Readable`` which is a module with a ``value`` and a ``status`` that can both
be read.  Additional capabilities like custom commands or parameters are not
excluded, this is a minimum set of things the Module has.  For a full
definition, have a look at :ref:`the specification <interface-classes>`.  The
``features`` field is similar to the interface classes, but Features are small
additions in functionality, that can be plugged into any of the interface
classes.  The description here can again give supplemental information about the
module.

.. code:: json

    "accessibles": {
      "value": {
        "description": "current value of the module",
        "datainfo": {
          "type": "double",
          "unit": "°C"
        },
        "description": "temperature outside",
        "readonly": true
      },
      "status": {
        "description": "current status of the module",
        "datainfo": {
          "type": "tuple",
          "members": [
            {
              "type": "enum",
              "members": {
                "IDLE": 100,
                "WARN": 200,
                "ERROR": 400
              }
            },
            { "type": "string" }
          ]
        },
        "readonly": true
      }
    }

The ``accessibles`` field lists all parameters that are defined on the module
and can be accessed over SECoP.  In the block above, you can see ``value`` and
``status`` two parameters which almost all modules will have.  The precise
semantics of all such parameters are defined in :ref:`the specification
<accessibles>`.

The value is the current value of the module, and the status is a two-element
tuple of a status code and a message that can give more information about the
module's current state.  Each parameter has a description and information about
data format, whether they can be written to, and more.

For the ``heater`` module, most things parallel the one before it, but there are
some differences:

It is a ``Drivable`` which comes with additional things:

- an additional status code ``BUSY``
- a ``target`` which is a writable parameter
- two commands (see below)
- a custom parameter ``_maxheaterpower``

Every parameter or command which is not defined by the interface class or a
feature has to be prefixed with an underscore.  This marks it as a custom name
to prevent future name clashes with the standard but otherwise, it follows the
same rules as a predefined parameter/command.

.. code:: json

    "_examplecommand": {
      "description": "Do some calculation.",
      "datainfo": {
        "type": "command",
        "argument": {
          "type": "struct",
          "members": {
            "a": {
              "min": 0.0,
              "max": 10.0,
              "type": "double"
            },
            "b": {
              "type": "double"
            }
          }
        },
        "result": {
          "type": "double"
        }
      }
    }

Commands are like functions that you can call on a module, they can have
arguments and results.  Here, we will only look at the ``_examplecommand``
command, since the predefined ``stop`` has no arguments and no result.  All the
information is included in the datainfo field.  Every command in SECoP can only
have a single argument.  To make multi-argument functions, one has to use either
a tuple or a struct, as shown above, where there are two named arguments ``a``
and ``b``.  These follow the same rules as the parameter datatype definitions.


~~~~~~~~~~~
Interaction
~~~~~~~~~~~

We now know the advertised capabilities of the SEC node, and armed with that
knowledge, we can interact with specific parts of it.


Reading values
^^^^^^^^^^^^^^

The most basic command to access a module is the :ref:`read <message-read>`
message, where we can retrieve the value of a parameter:

.. code::

    > read outside:value
    < reply outside:value [23.2, {"t": 1212121.1212121}]

We have to specify which ``module`` and ``parameter`` we want to access, and get
back an answer containing the value and so-called ``qualifiers`` which contain
:ref:`additional information <qualifiers>`.  Here, the only qualifier is ``t`` -
the timestamp of the read.


Writing values
^^^^^^^^^^^^^^

If we want to set a value, for example the ``_maxheaterpower`` of the ``heater``
we can use the :ref:`change <message-change>` message:

.. code::

    > change heater:_maxheaterpower 40.0
    < changed heater:_maxheaterpower [40.0, {"t": 1212121.1212121}]

As a reply, we get the feedback that the parameter was set.  If we try to set an
invalid value, we get back an error instead:

.. code::

    > change heater:_maxheaterpower 200
    < error_change heater:_maxheaterpower ["RangeError", "200.0 must be between 0 and 100", {}]

As you can see, errors use a different message name
(``error_<originalmessage>``) and include more information in the data part: an
error class (which is defined by :ref:`the specification <error-reply>`), an
error string giving more information, and some qualifiers (in this case, none).


Running commands
^^^^^^^^^^^^^^^^

Running a command is done with the :ref:`do <message-do>` message:

.. code::

    > do heater:stop
    < done heater:stop

As feedback that the command was run, we get back a ``done`` acknowledgment.
Again, we might get an ``error_do`` message instead that indicates that
something did not go as requested (or the request itself is bad).


Actions that take longer
^^^^^^^^^^^^^^^^^^^^^^^^

In SECoP, running commands or changing parameters does not block until the
physical action is done.  To explain, if you set the target parameter to 20K
above the current value, depending on what the heater actually heats, it may
take a while to heat up.  You would immediately get the feedback that the target
was changed, and you would then see the value going up as the hardware does its
job.  To know when the command or parameter change is completed, you have to
have a look at the status.  It will go ``BUSY`` until the change is done.  When
it returns to ``IDLE`` then the action is finished.

The other commands won't be discussed here, but as a pointer have a look at
:ref:`activate <message-activate>` which enables asynchronous mode.  That gives
you a stream of updates for all parameters of a SEC node without polling.


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Letting the computer do it for you
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Of course, the point of this protocol is to automate the communication with
your sample environment hardware. It would defeat the purpose if you sit at the
instrument all day, typing commands. Clients that can consume the description
can do the work for you. For some existing implementations, :doc:`have a look
at the implementations <../implementations/index>` or their respective
:doc:`starting guides <../getting-started/index>`. Or if you want to write your
own, please tell us, we'd love to hear about it!
