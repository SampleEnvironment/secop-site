============
Introduction
============

Here you will find a short overview of SECoP.

Background
~~~~~~~~~~

SECoP developed out of the need of multiple large scale facilities in the neutron science world to make equipment easier to share between facilities. This should not deter you from using it, as it's flexibility allows for a wide range of use cases.

.. metadata, why not x?, semantics, not just syntax, sine2020/hmc, machine/human readable
   talk slide 7
   philosophy talk slide 16
   word doc

Basics
~~~~~~

SECoP is a line-based protocol.

..
    Problems:

    Different Instrument Control Softwares with different ways to control SE
    Complex SE software interface protocols (Taco/Tango, EPICS…)
    Time consuming integration of new or external SE equipment (no easy mobility)

    No standard for SE metadata

    "…a common standard protocol for interfacing sample environment equipment to instrument control software.
    …compatible with a broad variety of soft- and hardware operated at the different LSF’s…
    …The adoption of this standard will greatly facilitate the installation of new equipment and the sharing of equipment between the facilities…
    …Implementations of the Sample Environment Communication Standard Protocol (SECoP) will then be tested at different facilities and provided to interested industrial partners for implementation…
    …In the context of SECoSP all sample environment related metadata has to be made available in a standard form
    Simple: all parts of SECoP (transport layer, syntax) should be as simple as possible (but as complex as needed).
    Inclusive: enable the use of SECoP by ECSs with a great variety of design concepts (e.g. synchronous vs. asynchronous communication).
    Self-explaining: the description of a SEC node must contain all necessary information for a) operating the SEC node by the ECS without further documentation in at least a basic mode, b) providing all relevant metadata information.
    Definitions: Necessary - sufficient – unambiguous, don’t define what does not have to be defined.
    Transport layer: byte oriented (TCP/IP, serial), ASCII
    Protocol is independent from specific transport layer.
    Complex functionality of the sample environment equipment (on the SEC-node side) is wrapped so that a simplified and standardized use of SE equipment by the ECS is possible.
    Basic SECoP plug-and-play operation must always be possible.
    Keep the overhead for the SECoP protocol on SEC node (server) side small.
    Avoid unnecessary traffic.
    Better to be explicit.
    All protocol messages must be human readable (with only exception: blob).
    Names in SECoP are treated as case sensitive but must be unique if lowercased.
    Use JSON.
    Impose best-practices to the programmer of the SEC node by making important features mandatory.
    Must ignore policy
    Allow for multiple clients.
    If multiple clients are connected to a SEC-node, only one of them should change parameters or send commands. Otherwise resulting problems might not be handled by SECoP.
    There should be a general way of doing things.
    why not mqtt etc.
    machine+human

SECNodes
~~~~~~~~

Implementing SECNodes is best done with one of the preexisting frameworks.

Depending on your background or the technologies already in use with your
facility, you can choose the :doc:`implemenation <../implementations/index>` that suits your needs best.
