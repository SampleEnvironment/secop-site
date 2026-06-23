===============
secant-service
===============

**secant-service** is a web-based SECoP client application built with
`Elixir <https://elixir-lang.org/>`_ and the
`Phoenix <https://www.phoenixframework.org/>`_ web framework.

.. image:: images/secant-service.svg
   :class: impl-logo

It connects to one or more SECNodes, persists the incoming parameter values in a
database, and exposes them through a browser interface.  The interface provides:

- **Node browser**: inspect the modules, parameters, and commands exposed by
  each connected SECNode.
- **Data browser**: query and browse stored parameter values over time.
- **Dashboard**: a live overview of the managed nodes and their current state.

secant-service can be run locally or deployed as a Docker container, making it
suitable both as a quick diagnostic tool during development and as a lightweight
data-logging service in a production environment.


Sources/Where to get
--------------------

`On GitHub <https://github.com/Bilchreis/secant-service>`_.
