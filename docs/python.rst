|pythonlogo| Leruli Python package
==================================

.. note:: Please feel free to `✎ improve this page <https://github.com/leruli-com/CLI/edit/master/docs/python.rst>`_ or to `🕮 ask questions about this page <https://github.com/leruli-com/CLI/discussions>`_.

.. |pythonlogo| image:: _static/images/python-brands.png
  :width: 30
  :alt: Python logo

You can install the ``leruli`` Python package via

.. code-block:: console

    $ pip install -U leruli

and make it available in your script via ``import leruli``.

Cheminformatics functions
-------------------------

.. autosummary::
   :nosignatures:

   leruli.canonical_formula 
   leruli.canonical_graph
   leruli.graph_to_formula
   leruli.graph_to_geometry
   leruli.graph_to_solvation_energy

Chemical space functions
------------------------


.. autosummary::
   :nosignatures:

   leruli.formula_to_graphs

Leruli Queue/Cloud functions
----------------------------

.. autosummary::
   :nosignatures:

   leruli.task_submit
   leruli.task_status
   leruli.task_cancel

All functions
-------------

.. automodule:: leruli
   :members:
   :undoc-members:
   :show-inheritance:
