===============
Implementations
===============

.. toctree::
    :maxdepth: 1
    :hidden:

    shall
    frappy
    octopy
    microsecop


..
  Frappy <https://github.com/SampleEnvironment/frappy>
  Octopy <https://gitlab.esss.lu.se/mesi/octopy>
  SHALL <https://github.com/SampleEnvironment/SHALL>

Here is a list of known implementations. For more information, have a look at
their respective pages.


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
constructing SECNodes.
The aim is for you to only program the parts relevant to communication with your
hardware, and letting the framework handle everything else.
Maybe you do not even need to code, since we have already written some drivers
that you can also use!
It also comes with a graphical client out of the box.


Octopy
~~~~~~

:doc:`Octopy <octopy>` is SECoP in a publish/subscribe, topics based environment:
an industrial IOT centered solution with an EPICS connection.
It builds its SECoP infrastructure upon MQTT and provides interfaces for easy
configuration like Node-red.


µSECoP
~~~~~~

:doc:`µSECoP <microsecop>` is an early-stage Rust implementation intended for
embedded usage, e.g. in microcontollers. There are existing examples for the
Esp32, the RP2040, and the Stm32.
