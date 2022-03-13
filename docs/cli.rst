|clilogo| Command Line Interface
================================

.. note:: Please feel free to `✎ improve this page <https://github.com/leruli-com/CLI/edit/master/docs/cli.rst>`_ or to `🕮 ask questions about this page <https://github.com/leruli-com/CLI/discussions>`_.


.. highlight:: shell

Installation
------------

To install Leruli CLI, run this command in your terminal:

.. code-block:: console

    $ pip install -U leruli

This is the preferred method to install Leruli CLI, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


.. |clilogo| image:: _static/images/terminal-solid.png
  :width: 30
  :alt: CLI logo

.. include:: ../README.rst

Cheminformatics
-------------------
.. click:: leruli.cli:canonical_formula
   :prog: leruli canonical-formula
   :nested: full 

.. click:: leruli.cli:canonical_graph
   :prog: leruli canonical-graph
   :nested: full 

.. click:: leruli.cli:graph_to_formula
   :prog: leruli graph-to-formula
   :nested: full 

.. click:: leruli.cli:graph_to_geometry
   :prog: leruli graph-to-geometry
   :nested: full 

.. click:: leruli.cli:graph_to_solvation_energy
   :prog: leruli graph-to-solvation-energy
   :nested: full 

.. click:: leruli.cli:graph_to_image
   :prog: leruli graph-to-image
   :nested: full 

Chemical Space
--------------

.. click:: leruli.cli:formula_to_cost
   :prog: leruli formula-to-cost
   :nested: full 

.. click:: leruli.cli:graph_to_name
   :prog: leruli graph-to-name
   :nested: full 

.. click:: leruli.cli:name_to_graph
   :prog: leruli name-to-graph
   :nested: full 

.. click:: leruli.cli:formula_to_graphs
   :prog: leruli formula-to-graphs
   :nested: full 

Physical Chemistry
------------------

.. click:: leruli.cli:graph_to_boiling_point
   :prog: leruli graph-to-boiling-point
   :nested: full 

.. click:: leruli.cli:graph_to_melting_point
   :prog: leruli graph-to-melting-point
   :nested: full 

.. click:: leruli.cli:graph_to_logP
   :prog: leruli graph-to-logp
   :nested: full 

.. click:: leruli.cli:graph_to_logD
   :prog: leruli graph-to-logd
   :nested: full 

.. click:: leruli.cli:graph_to_pKa
   :prog: leruli graph-to-pka
   :nested: full 


Cloud Compute
-------------

.. click:: leruli.cli:task_get
   :prog: leruli task-get
   :nested: full 


.. click:: leruli.cli:task_prune
   :prog: leruli task-prune
   :nested: full 

.. click:: leruli.cli:task_publish_code
   :prog: leruli task-publish-code
   :nested: full 

.. click:: leruli.cli:task_status
   :prog: leruli task-status
   :nested: full 

.. click:: leruli.cli:task_submit
   :prog: leruli task-submit
   :nested: full 

