Using the meaning property properly
===================================

Introduction
------------

The :obj:`meaning <mod.meaning>` property is a powerful mechanism in SECoP that provides structured semantic metadata about modules and accessibles. 
It enables machine-readable interpretation of experimental data and explicitly supports linking your data to external knowledge bases 
(for example ontologies, glossaries, and controlled vocabularies), making it easier to automatically identify what physical quantities 
are being measured or controlled and how they relate to your experiment.

For the normative field definitions, see :ref:`descriptive-data`, especially :obj:`module meaning property <mod.meaning>` and :obj:`parameter meaning property <meaning>`.

Why Use the Meaning Property?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Making Data FAIR**

The ``meaning`` property helps make data more FAIR by adding structured semantic context. By linking to
stable identifiers for ontology/vocabulary terms, data becomes easier to discover. Standardized function names and vocabulary links 
improve interoperability across systems, and clear semantic descriptions make experimental data easier to understand and reuse.

**Automated Data Interpretation**

The ``meaning`` property also enables automated interpretation workflows. It helps software identify sample-relevant 
parameters in complex setups, prioritize data streams based on importance, and connect measurements to domain-specific 
vocabularies and ontologies. This adds machine-readable context that does not depend solely on human interpretation of 
free-text descriptions.

What It Represents
~~~~~~~~~~~~~~~~~~

The ``meaning`` property provides semantic classification of the physical quantity or role a module or parameter serves, explicit 
relationships to the sample or broader experimental setup, and links to formal vocabularies or ontologies for precise definitions.

The ``meaning`` property does NOT replace the :obj:`description <description>` field, because human-readable context is still needed; the 
:obj:`datainfo <datainfo>` field, because type information and units remain separate; or interface classes, which define functional capabilities.

Core Explanation
----------------

Field Reference
~~~~~~~~~~~~~~~

To avoid duplicating normative specification text in this how-to, treat the
full field definitions as canonical in the specification:

- :obj:`module meaning property <mod.meaning>`
- :obj:`parameter meaning property <meaning>`

Fields at a glance:

.. list-table::
   :header-rows: 1
   :widths: 22 78

   * - Field
     - Short description
   * - ``function``
     - SECoP semantic function name describing what is measured or controlled
       (for example ``temperature`` or ``temperature_regulation``).
   * - ``importance``
     - Hierarchy/priority level ``0..50`` used for equipment context and data
       prioritization.
   * - ``belongs_to``
     - Relation target for the function context, typically ``"sample"`` or
       ``"other"``.
   * - ``link``
     - URI to an external ontology or controlled-vocabulary term.
   * - ``key``
     - Human-readable label associated with ``link`` in link-based meanings.

Valid Field Combinations
~~~~~~~~~~~~~~~~~~~~~~~~

The specification allows these specific field combinations::

  {function, importance, belongs_to}
  {function, importance}
  {key, link}
  {link}
  {function, importance, link}
  {function, importance, key, link}
  {function, importance, belongs_to, link}
  {function, importance, belongs_to, key, link}


.. note::
  
  - A valid ``meaning`` object must include at least ``function`` or ``link``.
  - ``importance`` and ``belongs_to`` are only valid together with ``function``.
  - ``key`` is only valid together with ``link``.
  - Use ``*_regulation`` functions only for regulation modules with at least
    ``Writable`` capability.

Meaning Structure Types
~~~~~~~~~~~~~~~~~~~~~~~

A valid ``meaning`` object must contain at least a ``link`` or a ``function`` field. There are three main approaches:

**Function-Based Meanings**

Uses predefined function names from the SECoP vocabulary, optionally with context information:

.. code:: json

  {"function": "temperature", "importance": 20}

**Link-Based Meanings**

References external vocabularies or ontologies:

.. code:: json

  {"link": "https://w3id.org/nfdi4cat/voc4cat_0000051"}

**Combined Meanings**

Connects SECoP functions with formal ontologies for maximum interoperability:

.. code:: json

  {
    "function": "temperature_regulation",
    "importance": 20,
    "belongs_to": "sample",
    "link": "https://w3id.org/nfdi4cat/voc4cat_0000051",
    "key": "synthesis temperature"
  }




Where Meaning Can Be Applied
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``meaning`` property can be defined at two levels in the SECoP structure:

**Module Level**

Applied to a module in its descriptive data, providing semantic information about what the entire module represents:

.. code:: json

    {
      "modules": {
        "sample_temp": {
          "description": "Sample temperature controller",
          "interface_classes": ["Drivable"],
          "meaning": {
            "function": "temperature_regulation",
            "importance": 30,
            "belongs_to": "sample"
          },
          "accessibles": { ... }
        }
      }
    }

**Parameter Level**

Applied to individual parameters within a module:

.. code:: json

    {
      "accessibles": {
        "value": {
          "description": "current temperature value",
          "datainfo": {"type": "double", "unit": "K"},
          "readonly": true,
          "meaning": {
            "function": "temperature",
            "belongs_to": "sample"
          }
        }
      }
    }

.. note:: The parameter-level meaning follows the same specification as the module-level meaning. The ``meaning`` property is not valid for commands.

Best Practices
~~~~~~~~~~~~~~

1. **Use both function and link when possible**: Combine SECoP's predefined functions with formal ontology references for maximum interoperability.

2. **Choose appropriate importance levels**: Accurately reflect the equipment hierarchy to help data analysis tools prioritize information.

3. **Prefer persistent term identifiers for links**: Use stable identifiers (for example, w3id.org or purl.obolibrary.org links) rather than potentially unstable domain-specific URLs.

4. **Be specific with belongs_to**: Mark parameters directly affecting the sample as ``"belongs_to": "sample"`` to enable automated sample-centric analysis.

5. **Use meaning at the right level**: Apply meaning to modules for general classification, and to accessibles when individual parameters have distinct semantic roles.

6. **Keep descriptions complementary**: The ``meaning`` provides machine-readable semantics; keep human-readable context in ``description``.

Common Pitfalls
~~~~~~~~~~~~~~~

**Invalid field combinations**: Ensure your field combination matches one of the allowed patterns. For example, ``key`` cannot exist without ``link``.

**Missing required fields**: Every meaning object must have at least ``link`` or ``function``.

**Meaning on commands**: The ``meaning`` property is only valid at module level and parameter level, not for commands.

**Wrong importance values**: Stay within the ``[0, 50]`` range and use values that represent the actual equipment hierarchy.

**Regulation without Writable**: Modules with ``_regulation`` functions must have at least the ``Writable`` interface class.

Examples
--------

Example 1: Basic Room Temperature Sensor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A simple temperature sensor monitoring room conditions at the instrument level:

.. code:: json

    "modules": {
      "room_temp": {
        "description": "Room temperature monitor",
        "interface_classes": ["Readable"],
        "meaning": {
          "function": "temperature",
          "importance": 10,
          "belongs_to": "other"
        },
        "accessibles": {
          "value": {
            "description": "current room temperature",
            "datainfo": {"type": "double", "unit": "degC"},
            "readonly": true
          }
        }
      }
    }

**Interpretation**: This is a temperature measurement (``function``) at the instrument/beamline level (``importance: 10``), not directly related to the sample (``belongs_to: "other"``).

Example 2: Sample Temperature Controller
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A temperature regulation system directly controlling the sample:

.. code:: json

    "modules": {
      "sample_heater": {
        "description": "Sample temperature controller",
        "interface_classes": ["Writable", "Drivable"],
        "meaning": {
          "function": "temperature_regulation",
          "importance": 30,
          "belongs_to": "sample"
        },
        "accessibles": {
          "value": {
            "description": "current sample temperature",
            "datainfo": {"type": "double", "unit": "K"},
            "readonly": true,
            "meaning": {
              "function": "temperature",
              "belongs_to": "sample"
            }
          },
          "target": {
            "description": "target sample temperature",
            "datainfo": {"type": "double", "unit": "K"},
            "readonly": false
          }
        }
      }
    }

**Interpretation**: The module performs temperature regulation (note the ``_regulation`` suffix) at the insert level (``importance: 30``), directly affecting the sample. The ``value`` accessible has its own meaning indicating it measures temperature.

Example 3: Magnetic Field with Ontology Link
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A magnet system linked to a formal ontology:

.. code:: json

    "modules": {
      "magnet": {
        "description": "Superconducting magnet system",
        "interface_classes": ["Writable", "Drivable"],
        "meaning": {
          "function": "magneticfield",
          "importance": 20,
          "belongs_to": "sample",
          "link": "https://purl.obolibrary.org/obo/PATO_0001035",
          "key": "magnetic flux density"
        },
        "accessibles": {
          "value": {
            "description": "current magnetic field",
            "datainfo": {"type": "double", "unit": "T"},
            "readonly": true
          }
        }
      }
    }

**Interpretation**: This combines SECoP's predefined ``magneticfield`` function with a link to the PATO (Phenotype and Trait Ontology), providing both machine-readable classification and formal ontological grounding.

Example 4: Ontology-Only Reference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A specialized parameter identified solely by an ontology reference:

.. code:: json

    "modules": {
      "rh_sensor": {
        "description": "Relative humidity sensor",
        "interface_classes": ["Readable"],
        "meaning": {
          "link": "https://purl.obolibrary.org/obo/ENVO_01001102",
          "key": "relative air humidity"
        },
        "accessibles": {
          "value": {
            "description": "relative humidity percentage",
            "datainfo": {"type": "double", "unit": "%"},
            "readonly": true
          }
        }
      }
    }

**Interpretation**: When a suitable SECoP function doesn't exist, you can use only a vocabulary link. This is particularly useful for specialized measurements.

Example 5: Complete Semantic Description
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A comprehensive example combining all elements:

.. code:: json

    "modules": {
      "synthesis_temp": {
        "description": "Synthesis temperature controller for catalysis experiments",
        "interface_classes": ["Writable", "Drivable"],
        "meaning": {
          "function": "temperature_regulation",
          "importance": 20,
          "belongs_to": "sample",
          "link": "https://w3id.org/nfdi4cat/voc4cat_0000051",
          "key": "synthesis temperature"
        },
        "accessibles": {
          "value": {
            "description": "current synthesis temperature",
            "datainfo": {"type": "double", "unit": "K"},
            "readonly": true
          },
          "target": {
            "description": "target synthesis temperature",
            "datainfo": {"type": "double", "unit": "K"},
            "readonly": false
          },
          "ramp": {
            "description": "temperature ramp rate",
            "datainfo": {"type": "double", "unit": "K/min"},
            "readonly": false
          }
        }
      }
    }

**Interpretation**: This provides the richest semantic description:

- SECoP classification: temperature regulation at the sample environment level
- Domain context: for sample-related measurements
- Formal ontology: linked to a catalysis-specific vocabulary
- Experimental context: identified as "synthesis temperature"

This enables both general-purpose SECoP tools and domain-specific applications to properly interpret the data.

Example 6: Multi-Module Setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A realistic setup showing the hierarchy in a complex system:

.. code:: json

    "modules": {
      "vti_temp": {
        "description": "VTI temperature sensor",
        "interface_classes": ["Readable"],
        "meaning": {
          "function": "temperature",
          "importance": 20
        }
      },
      "sample_temp": {
        "description": "Sample temperature regulation",
        "interface_classes": ["Writable", "Drivable"],
        "meaning": {
          "function": "temperature_regulation",
          "importance": 30,
          "belongs_to": "sample"
        }
      },
      "sample_sensor": {
        "description": "Direct sample temperature measurement",
        "interface_classes": ["Readable"],
        "meaning": {
          "function": "temperature",
          "importance": 30,
          "belongs_to": "sample"
        }
      },
      "room_temp": {
        "description": "Laboratory temperature",
        "interface_classes": ["Readable"],
        "meaning": {
          "function": "temperature",
          "importance": 10
        }
      }
    }

**Interpretation**: The ``importance`` values establish a hierarchy:

- Lab temperature (10): Environmental background
- VTI temperature (20): Sample environment infrastructure  
- Sample regulation and measurement (30): Direct sample-level measurements

Data analysis tools can automatically prioritize sample-level data while preserving context from the environment.

Further Reading
---------------

- See the full specification in :ref:`descriptive-data`, especially :obj:`module meaning property <mod.meaning>` and :obj:`parameter meaning property <meaning>`
- Related issues: :issue:`009 Module Meaning`, :issue:`026 More Module Meanings`
