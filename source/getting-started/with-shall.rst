Getting started: SHALL-LabVIEW
==============================

This section will give you an overview of the SHALL-LabVIEW integration for SECoP

The package allows the creation of SEC nodes in LabVIEW. It's interface is designed 
to be easily integrated into existing projects. The package uses the 
`SHALL <https://github.com/SampleEnvironment/SHALL>`_ libraries at its core to handle 
all SECoP communication and message handling.

**Note: The VIs in this project have been built using LabVIEW 2023. The Releases 
are also available for LabVIEW2019 in the Release Assets.**

Installation
------------

1. Getting the Source  
~~~~~~~~~~~~~~~~~~~~~

You can either clone the project directly, which will give you the latest version of 
the project, or select a `Release <https://github.com/SampleEnvironment/SHALL-LabVIEW/releases>`_ , 
where you can also download a version that has been exported for LabVIEW 2019.

Clone the Repository:
.. code:: bash
    
    git clone https://github.com/SampleEnvironment/SHALL-LabVIEW.git

Depending on your LabVIEW version you will able to use the Project as is, or export it 
for the specific version of LabVIEW you have installed.  

2. Setting Up the Platforms Folder 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order for the Qt libraries to work properly, a **softlink** must be created to the **platforms** folder 
(``PLATFORMS_PATH = ./shall-labview/[32bit|64bit]/platforms``) inside your LabVIEW installation directory. 

First, determine if you have the 32-bit or 64-bit version of LabVIEW installed. And where the installation 
directory is. From here on I will refer to the installation directory as ``LABVIEW_PATH``:

- **32bit** is usually located under:
    ``LABVIEW_PATH = C:\Program Files (x86)\National Instruments\LabVIEW 20XX``
- **64bit** is usually located under:
    ``LABVIEW_PATH = C:\Program Files\National Instruments\LabVIEW 20XX``


Next you also need the path ``PLATFORMS_PATH`` to the correct platforms folder :

- **LabVIEW 32bit** --> ``PLATFORMS_PATH = ...\shall-labview\32bit\platforms``
- **LabVIEW 64bit** -->  ``PLATFORMS_PATH = ...\shall-labview\64bit\platforms``


Finally, create the symbolic link inside the LabVIEW installation directory

.. code:: 

    mklink /d LABVIEW_PATH\platforms PLATFORMS_PATH

3. Check your installation 
~~~~~~~~~~~~~~~~~~~~~~~~~~

To check if your installation was successful, you can open the ``SECoP.lvproj`` project file and 
open ``random-demo/dcy03.vi`` before running the VI, the correct DLL path must be entered. 




It is the same as `PLATFORMS_PATH` minus the `/platforms` postfix. 
It should look something like this:

.. image:: https://github.com/user-attachments/assets/8659c9a4-fd4a-4949-a38d-d4110855eadf


.. code:: 

    D:\shall-repos\shall-labview\64bit

or

.. code:: 
    
    D:\shall-repos\shall-labview\32bit


If you entered the DLL path correctly and run the Vi, a small `SECoP Status` window should open. 



Creating a SEC Node
-------------------

For a detailed tutorial on how to create and manage SEC nodes using SHALL-LabVIEW 
please refer to the SHALL-LabVIEW `Wiki <https://github.com/SampleEnvironment/SHALL-LabVIEW/wiki>`_.




