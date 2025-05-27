.. _api_reference:

###
API
###


A list of all functions in the ``miblab`` python package. 

This package provides an API to *miblab* operations that are relevant 
across applications such as retrieving data or models, generating pdf 
reports, or deploying pipelines.

.. currentmodule:: miblab


*********
Reporting
*********

To access these functions, miblab must be installed with the `report` option:

.. code-block:: console

   pip install miblab[report]

All reporting functionality is wrapped up in a single class:

.. autosummary::
   :toctree: ../api/
   :template: custom-class-template.rst

   Report


****
Data
****

To access these functions, miblab must be installed with the `data` option:

.. code-block:: console

   pip install miblab[data]

APIs for upload and download to 
`Zenodo <https://zenodo.org/communities/miblab>`_ 
and 
`OSF <https://osf.io/un5ct/>`_:


.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   zenodo_fetch
   osf_fetch
   osf_upload


*****************
Deep learning API
*****************

To access these functions, miblab must be installed with the `dlseg` option:

.. code-block:: console

   pip install miblab[dlseg]

Interfaces for deploying deep learning models.

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   totseg
   kidney_pc_dixon
   kidney_dixon_fat_water
   
