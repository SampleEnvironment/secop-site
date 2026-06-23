Getting started: secant-service
================================

This section walks you through running secant-service using Docker.
secant-service connects to one or more SECNodes, persists incoming parameter
values in a PostgreSQL database, and exposes them through a browser interface.

- `secant-service Repository <https://github.com/Bilchreis/secant-service>`_

Prerequisites
-------------

You need `Docker <https://docs.docker.com/get-docker/>`_ with the Compose
plugin installed.  Verify with:

.. code:: bash

    docker compose version

Setup
-----

Clone the repository to get the ``docker-compose.yml`` and the example
configuration:

.. code:: bash

    git clone https://github.com/Bilchreis/secant-service.git
    cd secant-service

Configuration
-------------

After cloning the repository, everything is already configured to run out of
the box, so you can jump straight to `Starting secant-service`_ to try it out.

For a production deployment, the ``docker-compose.yml`` reads its configuration
from ``.env.example``.  Copy it and edit the values before starting:

.. code:: bash

    cp .env.example .env

Open ``.env`` in your editor.  The file contains the following variables:

.. code::

    POSTGRES_DB=secant_service_db
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    DATABASE_URL=ecto://postgres:postgres@db/secant_service_db
    SECRET_KEY_BASE=EXAMPLE_SECRET...
    TOKEN_SIGNING_SECRET=EXAMPLE_TOKEN_SIGNING_SECRET_CHANGE_ME
    PORT=4001
    DATA_RETENTION_DAYS=30
    TRASH_RETENTION_DAYS=7

The important variables to review:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Variable
     - Description
   * - ``POSTGRES_PASSWORD``
     - Password for the PostgreSQL user.  Change this for any non-local deployment.
   * - ``SECRET_KEY_BASE``
     - Phoenix application secret.  **Must** be replaced with a random value in production.
       Generate one with ``mix phx.gen.secret`` or any 64-byte random string.
   * - ``TOKEN_SIGNING_SECRET``
     - Secret used to sign API tokens.  **Must** be replaced in production.
   * - ``PORT``
     - Port on which the web interface is served (default ``4001``).
   * - ``DATA_RETENTION_DAYS``
     - How many days of parameter history to keep (default 30).
   * - ``TRASH_RETENTION_DAYS``
     - How many days deleted entries are kept before permanent removal (default 7).

.. note::

    After copying to ``.env``, update the ``env_file`` entries in
    ``docker-compose.yml`` from ``.env.example`` to ``.env``.
    The ``DATABASE_URL`` is already overridden inside ``docker-compose.yml``
    to route through the host's loopback interface, so that value does not
    need to be changed.

Starting secant-service
-----------------------

Start both the database and the application container:

.. code:: bash

    docker compose up -d

Docker will pull the ``ghcr.io/bilchreis/secant-service:latest`` image on the
first run.  Once both containers are healthy, the web interface is available at
``http://localhost:4001`` (or the ``PORT`` you configured).

.. note::

    secant-service uses **host networking** so that the SECoP UDP broadcast
    discovery on port 10767 can reach SECNodes on the local network.  This means
    the container binds directly to your host's network interfaces.

Stopping the service
--------------------

.. code:: bash

    docker compose down

Data stored in the PostgreSQL volume (``./postgres-data``) is preserved between
restarts.  To remove the volume as well, add the ``-v`` flag.
