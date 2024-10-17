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

TBD

Configuration
-------------

TBD
