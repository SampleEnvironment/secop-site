======
Frappy
======

Frappy is a Pyhon-based framework for writing both SECNodes and SECoP clients.

.. image:: images/frappy.svg
   :align: center

Workflow for SECNodes
~~~~~~~~~~~~~~~~~~~~~

You need at most three steps to a working SECNode:

1. Your driver implementation:
    Using the provided base-classes, you overwrite the functions that you need to customize to make your SECoP modules.
    Before you implement something yourself, have a look at the drivers that are already in the repository.
    Maybe the work was already done for you.

2. A configuration file for the server:
    To compose your modules together as parts of a SECNode, you write a simple configuration file.
    List all the modules you want to be part of the SECNode and fill in the required parameters and properties.

3. running the server
    Start the frappy-server and supply your configuration.

For a more detailed breakdown of the process while building an example, have a look at e.g. `this tutorial <https://forge.frm2.tum.de/public/doc/frappy/html/tutorial_t_control.html>`_.

How to get it
~~~~~~~~~~~~~
Source
------

You can find the source on `GitHub <https://github.com/SampleEnvironment/frappy>`_.

Packages
--------

There are RPM and debian packages uilt by us.

Windows builds can be found `here <https://forge.frm2.tum.de/public/>`_.

.. pypi once that has been resolved

Standalone Gui on Windows
-------------------------
For easier installation on Windows if you are using just the client, you can find a prebuilt executable `here <https://forge.frm2.tum.de/public/?p=frappy>`_.
