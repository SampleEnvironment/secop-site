Getting started: Frappy
=======================

This section will give you an overview of the Frappy implementation of SECoP.

Installation
------------

As a Python package, frappy is called ``frappy-core`` and can be installed with
the usual tools.  We recommend creating a `virtual environment
<https://docs.python.org/3/library/venv.html>`_ and then running ::

    pip install frappy-core

After that, you should be able to run ``frappy-server``:

.. code:: bash

    $ frappy-server
    usage: frappy-server [-h] [-v | -q] [-d] [-p PORT] [-c CFGFILES] [-g GENCFG] [-t] [-r] name
    frappy-server: error: the following arguments are required: name

The error is expected; the server expects to be called with the name of a
configuration, and we don't have configured anything yet.

And to configure a node and modules, we need to first write some code that
defines their behavior.

Writing components
------------------

Frappy is a framework that does most of the heavy lifting for you.
You define the functionality of the modules in Python classes.

To start, we create a very Basic Module that gives us a random value.
Import both Pythons standard ``random`` module and the ``Readable`` base class from frappy:

.. code:: python

    import random
    from frappy.core import Readable

The readable class already defines all parameters that are needed for a SECoP Readable.
To make our dice class, wie derive from the base and overwrite the

.. code:: python

    class Dice(Readable):
        def read_value(self):
            return random.randint(1, 6)

Save the python file to an appropriate location in your project.
For this tutorial, the location the guide will use is ``frappy_demo/dice.py'`` replace this with your files location.

Configuration
-------------

To start a server, we need two things: a general configuration file and the configuration for the SECNode.

General Configuration
~~~~~~~~~~~~~~~~~~~~~

For the general configuration, the file ``generalConfig.cfg`` is searched for in a few different places.
For now, create it in the folder where you want to run frappy, with the following contents.

.. code::

    [FRAPPY]
    logdir = ./log
    piddir = ./pid
    confdir = ./

This will tell frappy to put logfiles into a subdirectory called ``log``,
create a directory ``pid`` for keeping track of running daemons, and to search
for the SECNode configuration files in the current directory.

SECNode Configuration
~~~~~~~~~~~~~~~~~~~~~

The SECNode configuration for frappy is a normal Python file, with a few special calls that are available to use.
These are ``Node`` ``Mod`` and ``Param``.

There should be exactly one ``Node`` section, containing the configuration of
the SECNode. It receives the equipment id as it's first argument, the
description of the SECNode as its second, and the protocol and port of the main
interface as its third element.

.. code:: python

   Node('frappy_tutorial_node',
        'A SECNode for demonstrating frappy.',
        'tcp://10767'
   )

To configure a Module, we use the provided ``Mod`` call and supply it with at least three things:
The name of the module, the class that should be used and a description that is also sent in the SECNodes describe message.
Additionally, the configuration of parameters and properties is done with extra arguments.
Our dice does not have any yet, we will see that later.

.. code:: python

   Mod('d6',
        'frappy_demo.dice.Dice',
        'A six-sided dice example.',
   )

Change the second argument so that it points to the class you wrote in the step before.
You can save the config file at a point of you choosing. For example, as
``getting_started_cfg.py``. The ``_cfg.py`` part is the convention for frappy's
config file names. As the configuration files are just Python, you can make use
of loops, string formatting etc. to keep them concise.


Running the first example
-------------------------

To run the SECNode we just configured, run:

.. code:: bash

   $ frappy-server getting_started
   [10:00:00] frappy.getting_started           : waiting for modules being started
   [10:00:00] frappy.getting_started           : all modules started
   [10:00:00] frappy.getting_started.tcp       : TCPServer tcp binding to port 10767
   [10:00:00] frappy.getting_started.tcp       : TCPServer initiated
   [10:00:00] frappy.getting_started           : startup done with interface(s) tcp://10767

The output above shows a successful start. First, all modules are intialized
and started. Afterwards, the interfaces that we specified are created and start
to accept connections. You can try to connect to the SECNode now under port 10767.

.. dropdown:: Click to see the description.

    You should see something similar when you ask your SECNode for its description (just more compact).

    .. code::

       {
          "modules": {
            "d6": {
              "accessibles": {
                "value": {
                  "description": "current value of the module",
                  "datainfo": {
                    "type": "double"
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
                "pollinterval": {
                  "description": "default poll interval",
                  "datainfo": {
                    "unit": "s",
                    "min": 0.1,
                    "max": 120.0,
                    "type": "double"
                  },
                  "readonly": false
                }
              },
              "description": "A six-sided dice example.",
              "implementation": "frappy_demo.dice.Dice",
              "interface_classes": [
                "Readable"
              ],
              "features": []
            }
          },
          "equipment_id": "frappy_tutorial_node",
          "firmware": "FRAPPY 0.20.1",
          "description": "A SECNode for demonstrating frappy.",
          "_interfaces": [
            "tcp://10767"
          ]
        }

Congrats, you have your first running frappy SECNode!

A configurable module
---------------------

You may have noticed, that the dice in our first example returned a float instead of an integer, and that it hadthe number of sides fixed to six. Lets fix that. First, lets add some imports which we will use:

.. code:: python

    from frappy.core import Readable, Parameter, Property, IntRange


.. code:: python

    # in class Dice:
    value = Parameter(datatype=IntRange(1))

In order to set the correct datatype for the value, we can redefine ``value``
with just the keyword-argument datatype to override it without changing the
other properties like readonly. For that, we use the class IntRange, which
represents a SECoP ``int``.

Then, we declare a new Property ``sides``, which we use to configure the number
of sides of our dice:

.. code:: python

    # in class Dice:
    sides = Property('number of sides of the dice', IntRange(2),
                     default=6, export=True)

With ``IntRange(2)``, we constrain it to have a minimum value of two, as lower
numbers don't make sense for a die. With the default value of six, our old dice
module will still behave as a six-sided dice without a configuration change. We
set export to true so that we can see it through SECoP. By default, properties
of modules are not exported, as they are also used for internal configuration.

Lastly, we have to change the implementation of ``read_value`` to respect our new property:

.. code:: python

    # in class Dice:
    def read_value(self):
        return random.randint(1, self.sides)

Here you see, that you can use the values of parameters and properties within
your class code just as if it would be a normal Python class member.

This is how the class looks in the end:

.. code:: python

    from frappy.core import Readable, Parameter, Property, IntRange

    class Dice(Readable):
        value = Parameter(datatype=IntRange(1))
        sides = Property('number of sides of the dice', IntRange(2),
                         default=6, export=True)

    def read_value(self):
        return random.randint(1, self.sides)

To make a twenty-sided dice module, add the following to your configuration:

.. code:: python

    Mod('d20',
        'frappy_demo.dice.Dice',
        'Twenty-sided dice',
        sides = 20,
    )

Here, we configure the property to be 20. You can run the server again and now
you will have two modules, a six-sided and a twenty-sided die.

The demo SECNode
----------------

This part will show how the process of how to use the official demonstrator with frappy.

TBD
