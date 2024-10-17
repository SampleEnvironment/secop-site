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
    howtos/index
    implementations/index
    Spec 1.0 <specification/SECoP_Specification_V1.0>
    contact
    ISSE <https://sampleenvironment.org/>
    privacy-policy

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
   :gutter: 4

   .. grid-item::

      **Inclusive** means that facilities can use this protocol and don’t have to change
      their basic work flow.
      Circulating and integration of equipment will be made easier.

   .. grid-item::

      **Simple** means it should be easy to integrate and to use, by humans and computers,
      for example using text-based messages instead of binary formats.

   .. grid-item::

      **Self Explaining** means that SECoP transports the data, metadata *and* a human and machine readable
      description, which allows environment control software to configure itself.

The :doc:`Introduction <intro/index>` section has examples of the protocol, as
well as example code to get started with writing drivers using one of our
implementations.

See the :doc:`Specification <specification/index>` section for the full specification.

In :doc:`Implementations <implementations/index>` you can see the known implementations, which
cover a wide range of use cases and technologies.

Currently, as part of the project SECoP@HMC, the capabilities around metadata are extended to allow easier interfacing with metadata initiatives working further up the stack.

.. image:: _static/secophmc.svg
