Getting started: SECoP-Ophyd
==============================

This section will give you an introduction to the SECoP-Ophyd integration. 

For this purpose a demonstration project with simulated containerized sample environment hardware
has been created. It shows all necessary components needed to integrate a SECoP enabled sample 
environment into the `bluesky <https://blueskyproject.io/>`_ eco system. 

Installation
------------

First clone the repository of the demonstrator project:

.. code:: bash

    git clone https://codebase.helmholtz.cloud/rock-it-secop/secop-sim.git



.. note::  Running the demo on a Linux-based system is much easier, but it is also possible to run it on Windows. 
    on Windows, but the process is a bit more manual.

Linux:
~~~~~~

Make sure ``make`` and ``docker`` are installed. 


Then a single command is needed to install all the necessary dependencies, 
build and launch the Docker containers, and launch the frappy-gui client already 
connected to the containerised SEC nodes. It will take some time for everything 
to be set up the first time it is invoked.

.. code:: bash
    
    make frappy


Windows:
~~~~~~~~

The installation process is split up in these three steps:

1. Setting up the Demonstrator Virtual Environment ``venv``
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. code:: 

    python -m venv .venv
    .venv\Scripts\activate.bat
    pip install --upgrade pip
    pip install -r requirements.txt

2. Docker Containers
"""""""""""""""""""""
.. code:: 
    
    docker compose up --detach

3. Frappy Client
"""""""""""""""""""""
.. code:: 

    git submodule update --init
    cd frappy
    python -m venv ._venv
    ._venv\Scripts\activate.bat
    pip install -r requirements-gui.txt
    python bin/frappy-gui localhost:10800 localhost:10801 localhost:10802





Demo
------------

The demo is contained in the ``GasDosing_demo.ipynb`` notebook. It shows how to instaniate SECoP-Ophyd devices and use them, whithin bluesky plans.