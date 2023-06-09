.. _data-types:

Data info
=========

SECoP defines a very flexible data typing system. Data info structures are used to describe
the possible values of parameters and how they are serialized.
They may also impose restrictions on the usable values or amount of data.
The data info structure consists of the name of the datatype augmented by data-properties to pinpoint the exact meaning of the data to be described.

SECoP defines some basic data types for numeric quantities, like double_ and integer_.
An enum_ is defined for convenience of not having to remember the meaning of values from a reduced set.
A bool_ datatype is similar to a predefined enum_, but uses the JSON-values ``true`` and ``false``.
(Of course 0 should be treated as ``false`` and 1 as ``true`` if a bool value isn't using the JSON literals.)
For non-numeric types, a string_ and a blob_ are defined as well.

Furthermore, SECoP not only defines basic data types but also structured datatypes.
A tuple_ allows to combine a fixed amount of values with different datatypes in an ordered way to be used as one.
An array_ stores a given number of data elements having the same datatype.
A struct_ is comparable to a tuple_, with the difference of using named entries whose order is irrelevant during transport.

The limits, which have to be specified with the data info, are always inclusive,
i.e. the value is allowed to have one of the values of the limits.
Also, both limits may be set to the same value, in which case there is just one allowed value.

All data info structures are specified in the descriptive data in the following generic form:

.. image:: images/datatype.svg
    :alt: datatype ::= '{' datatype-name ':' '{' ( datatype-property ( ',' datatype-property )* )? '}'


Here is an overview of all defined data types:


Depending on the data type, there are different sets of data-properties available.

.. _double:

Floating Point Numbers: ``double``
----------------------------------

Datatype to be used for all physical quantities.

.. note::
    The ECS SHOULD use internally IEEE-754 double floating point values and MUST support AT LEAST
    the full IEEE-754 single float value range and precision. However, NaN, infinite and
    denormalized numbers do not need to be supported, as JSON can't transport those 'values'.

    If the relative resolution is not given or not better than 1.2e-7, single precision floats
    may be used in the ECS.

    .. admonition:: Related Issue

       `SECoP Issue 42: Requirements of datatypes`_


Optional Data Properties
~~~~~~~~~~~~~~~~~~~~~~~~

``"min"``
    lower limit. if min is omitted, there is no lower limit

``"max"``
    upper limit. if max is omitted, there is no upper limit

.. note::
    When a SEC Node receives a ``"change"`` or ``"do"`` message with a value outside
    the allowed range [``"min"``, ``"max"``], it MUST reply with an error message.
    For readonly parameters, [``"min"``, ``"max"``] indicate a trusted range.
    A SEC-Node might send ``"update"`` or ``"reply"`` messages with values outside
    the trusted range, for example when the value is an extrapolation of the
    calibrated range. The idea behind this relaxed rule is, that it is better
    for a SEC-node to send an acquired value outside the range as it is - rather
    than change its value just to comply with the specified range.
    The decision, how to treat such values is left to the ECS.

``"unit"``
    string giving the unit of the parameter.

    SHOULD be given, if meaningful. Unitless if omitted or empty string.
    Preferably SI-units (including prefix) SHOULD be used.

    .. admonition:: Related Issue

       `SECoP Issue 43: Parameters and units`_

``"absolute_resolution"``
    JSON-number specifying the smallest difference between distinct values.
    default value: 0

``"relative_resolution"``
    JSON-number specifying the smallest relative difference between distinct values:

    ``abs(a-b) <= relative_resolution * max(abs(a),abs(b))``

    default value: 1.2e-7 (enough for single precision floats)

    if both ``absolute_resolution`` and ``relative_resolution`` are given, the expected
    resolution is:

    ``max(absolute_resolution, abs(value) * relative_resolution)``

    .. admonition:: Related Issue

       `SECoP Issue 49: Precision of Floating Point Values`_

``"fmtstr"``
    string as a hint on how to format numeric parameters for the user.
    default value: "%.6g"

    The string must obey the following syntax:

    .. image:: images/fmtstr.svg
        :alt: fmtstr ::= "%" "." [1-9]? [0-9] ( "e" | "f" | "g" )


Example
~~~~~~~

.. code:: json

   {"type": "double", "min": 0, "max": 100, "fmtstr": "%.3f"}

Transport
~~~~~~~~~
as JSON-number

example: ``3.14159265``

.. _scaled:

Scaled Integer: ``scaled``
--------------------------

Scaled integers are to be treated as 'double' in the ECS, they are just transported
differently. The main motivation for this datatype is for SEC nodes with limited
capabilities, where floating point calculation is a major effort.


Mandatory Data Properties
~~~~~~~~~~~~~~~~~~~~~~~~~

``"scale"``
    a (numeric) scale factor to be multiplied with the transported integer

``"min"``, ``"max"``
    The limits of the transported integer. ``<min>`` <= ``<max>``.
    The limits of the represented floating point value are ``<min>*<scale>, <max>*<scale>``
    See also the note on the ``"min"`` and ``"max"`` properties of the  datatype.

Optional Data Properties
~~~~~~~~~~~~~~~~~~~~~~~~

``"unit"``
    string giving the unit of the parameter. (see datatype )

``"absolute_resolution"``
    JSON-number specifying the smallest difference between distinct values.

    default value: ``<scale>``

``"relative_resolution"``
    JSON-number specifying the smallest relative difference between distinct values:

    ``abs(a-b) <= relative_resolution * max(abs(a),abs(b))``

    default value: 1.2e-7 (enough for single precision floats)

    if both ``absolute_resolution`` and ``relative_resolution`` are given, the expected
    resolution is:

    ``max(absolute_resolution, abs(value) * relative_resolution)``

    .. admonition:: Related Issue

       `SECoP Issue 49: Precision of Floating Point Values`_

``"fmtstr"``
    string as a hint on how to format numeric parameters for the user.
    default value: "%.<n>f" where <n> = max(0,-floor(log10(scale)))

    The string must obey the same syntax as above for .

Example
~~~~~~~
.. code:: json

   {"type": "scaled", "scale": 0.1, "min": 0, "max": 2500}

i.e. a value between 0.0 and 250.0.

Transport
~~~~~~~~~
an integer JSON-number

for example ``1255`` meaning 125.5 in the above example.

.. admonition:: Related Issue

   `SECoP Issue 44: Scaled integers`_.

.. _int:
.. _integer:

Integer: ``int``
----------------

Datatype to be used for integer numbers.
For any physical quantity double_ or scaled_ **SHOULD** be used.
An int_ SHOULD have no unit and it SHOULD be representable with signed 24 bits (i.e. all integers SHOULD fit
inside -2\ :sup:`24` ... 2\ :sup:`24`), as some JSON libraries might parse JSON-numbers
with 32bit float too.

Mandatory Data Properties
~~~~~~~~~~~~~~~~~~~~~~~~~
``"min"``, ``"max"``
   integer limits, ``<min>`` <= ``<max>``

Optional Data Properties
~~~~~~~~~~~~~~~~~~~~~~~~

``"unit"``
    string giving the unit of the parameter. (see datatype Double_)

Example
~~~~~~~
.. code:: json

   {"type": "int", "min": 0, "max": 100}

Transport
~~~~~~~~~
as JSON-number

example: ``-55``

.. _bool:
.. _boolean:

Boolean: ``bool``
-----------------

Syntax
~~~~~~

.. code:: json

   {"type": "bool"}

Transport
~~~~~~~~~
``true`` or ``false``


.. _enum:

Enumerated Type: ``enum``
-------------------------

Mandatory Data Property
~~~~~~~~~~~~~~~~~~~~~~~
``"members"``
    a JSON-object: ``{<name>: <value>, ...}``

    ``name``\ s are strings, ``value``\ s are (small) integers, both ``name``\ s and ``value``\ s MUST be unique

Example
~~~~~~~

.. code:: json

   {"type": "enum", "members": {"IDLE": 100, "WARN": 200, "BUSY": 300, "ERROR": 400}}

Transport
~~~~~~~~~
as JSON-number, the client may perform a mapping back to the name

example: ``200``


.. _string:

String: ``string``
------------------

Optional Data Properties
~~~~~~~~~~~~~~~~~~~~~~~~

``"maxchars"``
    the maximum length of the string in UTF-8 code points, counting the number of characters (**not** bytes!)

    .. note::
        An UTF-8 encoded character may occupy up to 4 bytes.
        Also the end-of-string marker may need another byte for storage.

``"minchars"``
    the minimum length, default is 0

``"isUTF8"``
    boolean, if UTF8 character set is allowed for values, or if the value is allowed only
    to contain 7-bit ASCII characters (i.e. only code points < 128), each occupying a single byte.
    Defaults to **false** if not given.

Example
~~~~~~~

.. code:: json

   {"type": "string", "maxchars": 80}

Transport
~~~~~~~~~
as JSON-string

example: ``"Hello\n\u2343World!"``

.. _blob:

Binary Large Object: ``blob``
-----------------------------

Mandatory Data Property
~~~~~~~~~~~~~~~~~~~~~~~
``"maxbytes"``
    the maximum length, counting the number of bytes (**not** the size of the encoded string)

Optional Data Property
~~~~~~~~~~~~~~~~~~~~~~
``"minbytes"``
   the minimum length, default is 0

Example
~~~~~~~

.. code:: json

   {"type": "blob", "min": 1, "max": 64}

Transport
~~~~~~~~~
as single-line base64 (see :RFC:`4648`) encoded JSON-string

example: ``"AA=="`` (a single, zero valued byte)

.. _array:

Sequence of Equally Typed Items : ``array``
-------------------------------------------

Mandatory Data Properties
~~~~~~~~~~~~~~~~~~~~~~~~~

``"members"``
    the datatype of the elements

``"maxlen"``
    the maximum length, counting the number of elements

Optional Data Property
~~~~~~~~~~~~~~~~~~~~~~

``"minlen"``
    the minimum length, default is 0

Example
~~~~~~~

.. code:: json

   {"type": "array", "min": 3, "max": 10, "members": {"type": "int", "min": 0, "max": 9}}

Transport
~~~~~~~~~
as JSON-array

example: ``[3,4,7,2,1]``

.. _tuple:

Finite Sequence of Items with Individually Defined Type: ``tuple``
------------------------------------------------------------------

Mandatory Data Property
~~~~~~~~~~~~~~~~~~~~~~~
``"members"``
    a JSON array listing the datatypes of the members

Example
~~~~~~~

.. code:: json

   {"type": "tuple", "members": [{"type": "int", "min": 0, "max": 999}, {"type": "string", "maxchars": 80}]}

Transport
~~~~~~~~~
as JSON-array

.. code:: json

   [300,"accelerating"]


.. _Struct:

Collection of Named Items: ``struct``
-------------------------------------

Mandatory Data Property
~~~~~~~~~~~~~~~~~~~~~~~
``"members"``
    a JSON object containing the names and datatypes of the members

Optional Data Property
~~~~~~~~~~~~~~~~~~~~~~
``"optional"``
    The names of optional struct elements. When "optional" is omitted, all struct elements are optional.
    This means that a SEC node not implementing partial structs has to specify ``optional=[]`` in all structs.

    In 'change' and 'do' commands, the ECS might omit these elements,
    all other elements must be given.
    The effect of a 'change' action with omitted elements should be the same
    as if the current values of these elements would have been sent with it.
    The effect of a 'do' action with omitted elements is defined by the implementation.

    In all other messages (i.e. in replies and updates), all elements have to be given.

Example
~~~~~~~

.. code:: json

   {"type": "struct", "members": {"y": {"type": "double"}, "x": {"type": "enum", "members": {"On": 1, "Off": 0}}}}

Transport
~~~~~~~~~
as JSON-object

example: ``{"x": 0.5, "y": 1}``

.. admonition:: Related Issue

   `SECoP Issue 35: Partial structs`_


.. _command:

Command-flag for Accessibles
----------------------------

If an accessible is a command, its argument and result is described by the ``command`` datatype.

Optional Data Properties
~~~~~~~~~~~~~~~~~~~~~~~~

``"argument"``
    the datatype of the single argument, or ``null``.

    only one argument is allowed, though several arguments may be used if
    encapsulated in a structural datatype (struct_ or tuple_).
    If such encapsulation or data grouping is needed, a struct SHOULD be used.

``"result"``
    the datatype of the single result, or ``null``.

    In any case, the meaning of result and argument(s) SHOULD be written down
    in the description of the command.

Example
~~~~~~~

.. code:: json

   {"type": "command", "argument": {"type": "bool"}, "result": {"type": "bool"}}


Transport Example
~~~~~~~~~~~~~~~~~
Command values are not transported as such. But commands may be called (i.e. executed) by an ECS.
Example:

.. code::

    > do module:invert true
    < done module:invert [false,{t:123456789.2}]



.. _`Interface Classes and Features`: Interface%20Classes%20and%20Features.rst
.. DO NOT TOUCH --- following links are automatically updated by issue/makeissuelist.py
.. _`SECoP Issue 3: Timestamp Format`: issues/003%20Timestamp%20Format.rst
.. _`SECoP Issue 4: The Timeout SEC Node Property`: issues/004%20The%20Timeout%20SEC%20Node%20Property.rst
.. _`SECoP Issue 6: Keep Alive`: issues/006%20Keep%20Alive.rst
.. _`SECoP Issue 7: Time Synchronization`: issues/007%20Time%20Synchronization.rst
.. _`SECoP Issue 8: Groups and Hierarchy`: issues/008%20Groups%20and%20Hierarchy.rst
.. _`SECoP Issue 9: Module Meaning`: issues/009%20Module%20Meaning.rst
.. _`SECoP Issue 26: More Module Meanings`: issues/026%20More%20Module%20Meanings.rst
.. _`SECoP Issue 35: Partial structs`: issues/035%20Partial%20Structs.rst
.. _`SECoP Issue 36: Dynamic units`: issues/036%20Dynamic%20units.rst
.. _`SECoP Issue 37: Clarification of status`: issues/037%20Clarification%20of%20status.rst
.. _`SECoP Issue 38: Extension mechanisms`: issues/038%20Extension%20mechanisms.rst
.. _`SECoP Issue 42: Requirements of datatypes`: issues/042%20Requirements%20of%20datatypes.rst
.. _`SECoP Issue 43: Parameters and units`: issues/043%20Parameters%20and%20units.rst
.. _`SECoP Issue 44: Scaled integers`: issues/044%20Scaled%20integers.rst
.. _`SECoP Issue 49: Precision of Floating Point Values`: issues/049%20Precision%20of%20Floating%20Point%20Values.rst
.. _`SECoP Issue 59: set_mode and mode instead of some commands`: issues/059%20set_mode%20and%20mode%20instead%20of%20some%20commands.rst
.. DO NOT TOUCH --- above links are automatically updated by issue/makeissuelist.py
