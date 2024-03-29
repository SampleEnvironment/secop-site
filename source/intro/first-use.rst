=========
First Use
=========

So you have never used SECoP, and want to interact with a node?
For exploring the protocol, all you need is a program that can talk tcp or serial, depending on your device.
Connect to your device and send the following message to start communication ('>' and '<' show who is sending the message):

.. code::

    > *IDN?

The SECNode replies with the version number of the protocol that it wants to speak:

.. code::

    < ISSE,SECoP,V2019-09-16,v1.0

Great!
So we know, that we are talking to something that knows SECoP, but we do not know yet, what we are talking to.
That is, what we will find out with next message:

.. code::

    > describe

We will format the answer a bit, since it is longer than the usual messages we will encounter:

.. code::

    < describing . {
        "equipment_id": "introduction_node",
        "description": "a basic example",
        "modules": {
          "outside": {
            "interface_classes": ["Readable"],
            "implementation": "example.sensors.Temperature",
            "accessibles": {
              "description": {
                "value": {
                  "datainfo": {
                    "type": "double",
                    "unit": "C"
                  },
                  "description": "temperature outside",
                  "readonly": true
                }
              }
            }
          }
        }
      }

We asked the SECNode to describe itself to us, and now we can interact with specific parts of the SECNode.
The easiest command to access a module is the `read` command, where we have to say, which value we want to read:

.. code::

   > read outside:value
   < reply outside:value [23.2, {"t": 1212121.121221}]
