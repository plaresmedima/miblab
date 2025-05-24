.. _dlseg:

*******************************
Segmentation with deep learning
*******************************

A consistent interface for image segmentation with pretrained 
deep learning models from different libraries. 

This library purely provides wrappers for easy integration across miblab 
application areas. Please cite the original library when using any 
of these models (see function docstrings). 

To access these functions, miblab must be installed with the `dlseg` option:

.. code-block:: console

   pip install miblab[dlseg]


.. autofunction:: miblab.totseg

.. autofunction:: miblab.kidney_pc_dixon