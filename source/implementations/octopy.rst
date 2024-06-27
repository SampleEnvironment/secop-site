======
Octopy
======
..
    Octopy is SECoP in a publish/subscribe, topics based environment:
    an industrial IOT centered solution with an EPICS connection.
    It builds its SECoP infrastructure upon MQTT and provides interfaces for easy
    configuration like Node-red.

Octopy is an SECoP implementation based on MQTT.

.. image:: ../specification/images/secop-img/implementations-octopy.svg
   :align: center

Instead of a client-server approach Octopy internally and externally transports SECoP JSON formatted messages, data report, structure report and error reports, over MQTT.
Hardware connects to Octopy  either through drivers or directly if it has embedded MQTT support.
On the ECS side the messages are accessible through a standard client-server connection.
Octopy now also supports EPICS communication, both as a driver available for EPICS hardware as well as for ECS communicating through EPICS (pva).

Workflow
--------

1. Install Octopy and the needed components.
2. Have hardware publish data as SECoP data report on a topic. Gateways for TCP/IP, GPIB and EPICS exists and can be setup from Ink.
3. Use Ink to create, visualize and publish an extended SECoP structure report with the topic added.
4. The ECS gateways picks up the structure report, subscribes to the data and starts forwarding it to the ECSs.

Development is happening in the `ESS's GitLab <https://gitlab.esss.lu.se/mesi/octopy>`_.

