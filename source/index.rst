:html_theme.sidebar_secondary.remove:

=================
Welcome to SECoP!
=================

.. toctree::
    :maxdepth: 1
    :hidden:

    intro/index
    getting-started/index
    specification/index
    Spec 1.0 <specification/SECoP_Specification_V1.0>
    howtos/index

.. toctree::
    :maxdepth: 1
    :hidden:

    implementations/index

.. toctree::
    :maxdepth: 1
    :hidden:

    contact
    ISSE <https://sampleenvironment.org/>
    impressum

.. grid::

   .. grid-item::
      :columns: 4

      .. code-block::
         :class: intro-code-block

         > describe
         < describing secop {"..."}

   .. grid-item::

      The SECoP (Sample Environment Communication Protocol) is an Inclusive, Simple
      and Self Explaining (ISSE) communication protocol, intended as a common standard
      for interfacing sample environment equipment and instrument control software.
      It is, coincidentally, developed by `ISSE
      <https://sampleenvironment.org/>`_.


.. grid::

   .. grid-item::

   .. grid-item::

      .. button-ref:: intro/index
         :color: warning
         :shadow:

         See examples

   .. grid-item::

      .. button-ref:: specification/index
         :color: info
         :shadow:

         Read the spec

   .. grid-item::

      .. button-ref:: implementations/index
         :color: danger
         :shadow:

         Download code

   .. grid-item::

.. grid::
   :gutter: 5

   .. grid-item::

      **Inclusive** means that facilities can use this protocol and don’t have to change
      their work flow (rewrite drivers completely or organize and handle hardware in a
      specific way to fulfill SECoP requirements).


   .. grid-item::

      **Simple** means it should be easy to integrate and to use.

   .. grid-item::

      **Self Explaining** means that with SECoP, not only the pure data is transported. It
      also transports a human and machine readable description, which allows environment control software to configure by itself.


   .. grid-item::

      **Metadata**: sample environment related metadata is made available and accessible in a standard form.

   .. grid-item::
      circulating and integration of equipment will be made easier.

The :doc:`Introduction <intro/index>` section has examples of the protocol, as
well as example code to get started with writing drivers using one of our
implementations.

See the :doc:`Specification <specification/index>` section for the full specification.

In :doc:`Implementations <implementations/index>` you can see the known implementations, which
cover a wide range of use cases and technologies.

Currently, as part of the project SECoP@HMC, the capabilities around metadata are extended to allow easier interfacing with metadata initiatives working further up the stack.

.. image:: _static/secophmc.svg
