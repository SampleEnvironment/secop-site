=====
Tools
=====

.. toctree::
    :maxdepth: 1
    :hidden:

    shall
    frappy
    octopy
    microsecop
    secop-ophyd
    secant-service


The SECoP ecosystem contains quite a few different tools to create, connect to,
and visualize SECoP enabled hardware.


Implementations
---------------

These packages implement the full SECoP protocol and provide both server and
client libraries.


SHALL
~~~~~

The :doc:`SHALL library <shall>` is a C++/Qt based library implementing SECoP.
It can be used for programming SECNodes in C, C++ and other languages compatible
with the C-interface.
In particular, a LabView binding is provided for easy integration of SECoP into
existing LabView projects.


Frappy
~~~~~~

:doc:`Frappy <frappy>` is a Python-based framework that provides a basis for
constructing SECNodes.  The aim is for you to only program the parts relevant to
communication with your hardware, and letting the framework handle everything
else.  Maybe you do not even need to code, since we have already written some
drivers that you can also use.

It also comes with a client libraries and a ready graphical client out of the
box.


Octopy
~~~~~~

:doc:`Octopy <octopy>` is SECoP in a publish/subscribe, topics based
environment: an industrial IOT centered solution with an EPICS connection.  It
builds its SECoP infrastructure upon MQTT and provides interfaces for easy
configuration like Node-RED.


µSECoP
~~~~~~

:doc:`µSECoP <microsecop>` is an early-stage Rust implementation intended for
embedded usage, e.g. in microcontollers. There are existing examples for the
Esp32, the RP2040, and the Stm32.


Clients
-------

These packages are dedicated clients to connect to SECoP nodes, or can use SECoP
among other options.

secant-service
~~~~~~~~~~~~~~

:doc:`secant-service <secant-service>` is SECoP client built with
Elixir/Phoenix.  It connects to one or more SEC Nodes, persists their parameter
values in a database, and provides a web-interface for live plotting, control, 
and browsing of historic data.


NICOS
~~~~~

The `NICOS instrument control system <https://nicos-controls.org/>`_ has
built-in support for controlling SECoP, using frappy as a library to connect to
SEC nodes and present their modules as NICOS devices.


secop-ophyd
~~~~~~~~~~~

:doc:`secop-ophyd <secop-ophyd>` integrates SECoP hardware into the Bluesky
experiment orchestration framework.  It automatically generates
`ophyd-async <https://blueskyproject.io/ophyd-async/main/index.html>`_ device
objects from a SECNode's descriptive data, so SECoP modules can be used in
Bluesky plans alongside EPICS, Tango, and other backends without any
hand-written device definitions.


Other tools
-----------

secop-checker
~~~~~~~~~~~~~

`secop-checker <https://github.com/SampleEnvironment/secop-checker>`_ is a
work-in-progress tool to check the :ref:`static metadata <descriptive-data>` of
a SEC node against :ref:`YAML schemata <schemata>` that define the API for all
the different SECoP entities contained in it.

In short, it enables you to easily make sure your SEC nodes are standards
compliant.


Spin
~~~~

`Spin <https://forge.frm2.tum.de/public/doc/spin/master/>`_ is a status
visualization/HMI tool that presents information .  It has built-in support for
SECoP nodes and modules among other control systems.
