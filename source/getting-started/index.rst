===============
Getting Started
===============

If you like, you can have a look at how SECoP looks "on the wire", that is, what
messages are transferred over the connection between client and node.  This is
useful for building your own node or client.

.. toctree::
    :maxdepth: 1

    first-use

The following sections will show you the basics of installing existing server
softare and setting up your first SEC node using it.

Frappy is a Python framework for building SEC nodes and runs on any major
operating system.

.. toctree::
    :maxdepth: 1

    with-frappy

SHALL is a C++/Qt library to create nodes, which can be called via a C-compatible
interface.

.. toctree::
    :maxdepth: 1

    with-shall

Octopy is best at using SECoP within an MQTT environment.

.. toctree::
    :maxdepth: 1

    with-octopy

Use SECoP-ophyd to integrate SECoP devices in your Bluesky/Ophyd based control
system.

.. toctree::
    :maxdepth: 1

    with-secop-ophyd

secant-service is a web-based SECoP client that connects to SECNodes, logs
parameter values to a database, and provides a browser interface for browsing
and querying the data.

.. toctree::
    :maxdepth: 1

    with-secant-service
