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
For this tutorial, the location the guide will use is ``frappy_demo.dice'`` replace this with your files location.

Configuration
-------------

The configuration for frappy is a normal Python file, with a few special calls that are available to use.
These are ``Node`` ``Mod`` and ``Param``

There should be exactly one ``Node`` section, containing the configuration of the SECNode.
It receives the equipment id as it's first argument, the description of the SECNode as its second, and the protocol and port of the main interface as its third element.

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

You can save the config file at a point of you choosing. For example, as ``getting_started_cfg.py``.
The ``_cfg.py`` part is the convention for frappy's config file names.
As the configuration files are just Python, you can make use of loops, string formatting etc. to keep them concise.


Running the first example
-------------------------

To run the SECNode we just configured, run:

.. code:: bash

   $ frappy-server getting_started


TBD

The demo SECNode
----------------

This part will show how the process of how to use the official demonstrator with frappy.

TBD
