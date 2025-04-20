.. _api_reporting:

*********
Reporting
*********

.. currentmodule:: miblab.report

This module provides functions to generate pdf reports in 
miblab style. Basic usage is as follows:

.. code-block:: python

   import miblab.report as report

   # Where to save the report
   path = 'path/to/report/folder'

   # Setup the report
   doc = report.setup(path, title='My Report', author='Me')

   # Add a chapter
   report.chapter(doc, 'Chapter 1')

   # Add a figure
   report.figure(doc, 'figure.png', caption='This is a figure.')

   # Add a table
   report.table(doc, 'table.csv', caption='This is a table.')

   # Build the report
   report.build(doc, path)




.. autosummary::
   :toctree: ../generated/api/
   :template: autosummary.rst

   setup
   chapter
   figure
   table
   build





