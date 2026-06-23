===========
secop-ophyd
===========

**secop-ophyd** integrates SECoP-enabled hardware into the
`Bluesky <https://blueskyproject.io/>`_ experiment orchestration framework.

.. image:: images/secop-ophyd.svg
   :class: impl-logo

It acts as a bridge between SECoP nodes and Bluesky's
`ophyd-async <https://blueskyproject.io/ophyd-async/main/index.html>`_ device
layer: connecting to a SECNode via TCP, reading its descriptive data, and
automatically generating ophyd device objects for all exposed modules and
parameters.  The resulting devices can be used in
`Bluesky plans <https://blueskyproject.io/bluesky/main/tutorial.html#the-run-engine-and-plans>`_
just like any other ophyd device, giving SECoP hardware seamless access to the
full Bluesky ecosystem alongside EPICS, Tango, and other control-system
backends.

Communication with the SECNode is handled internally by
`Frappy <https://github.com/SampleEnvironment/frappy>`_.


Sources/Where to get
--------------------

`On GitHub <https://github.com/SampleEnvironment/secop-ophyd>`_.

secop-ophyd is also available on `PyPI <https://pypi.org/project/secop-ophyd>`_
and can be installed with ``pip install secop-ophyd``.

Full documentation is available at
`sampleenvironment.github.io/secop-ophyd <https://sampleenvironment.github.io/secop-ophyd/>`_.
