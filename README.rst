==========
Leruli CLI
==========

Use `leruli.com <https://leruli.com>`_ from both command line and within Python code: a convenience wrapper around the corresponding `API <https://api.leruli.com>`_.

Features
--------

Cheminformatics

* *graph-to-solvation-energy*: Estimate the free energy of solvation in kcal/mol.
* *graph-to-geometry*: Returns an approximate 3D geometry from a given graph input.
* *graph-to-formula*: Calculates the chemical formula in the Hill system given a graph representation like SMILES.
* *canonical-formula*: Expands nested or ill-ordered chemical formulas to conform to the Hill system.)
* *canonical-graph*: Returns a canonical version of the input graph-based representation.

Chemical space

* *formula-to-graphs*: Returns a list of up to 12 known molecules that are relevant for the given sum formula.
* *graph-to-name*: SMILES string to IUPAC name
* *name-to-graph*: IUPAC or trivial name to SMILES

Compute

* *formula-to-cost*: Estimates the resources required for a single point calculation of a given sum formula and basis set.
* *graph-to-boiling-point*: Predicts a boiling point in deg C.
* *graph-to-logD*: Predicts logD.
* *graph-to-logP*: Predicts logP.
* *graph-to-melting-point*: Predicts a melting point in deg C.
* *graph-to-pKa*: Predicts the pKa.

Images

* *graph-to-image*: Renders a molecule as SVG, PNG, or PDF

Arguments and usage are explained  `in the documentation <https://api.leruli.com>`_.


Examples for command line usage
-------------------------------

.. code-block::

   $ leruli name-to-graph acetone
   CC(=O)C
   
   $ leruli graph-to-geometry "CC(=O)C"
   10
   Generated with https://api.leruli.com/latest/references/BCE2020,BEG2019,rdkit/bibtex
   C -1.27026192165113 0.14084775426444 0.00476447523142
   C 0.02515865734774 -0.50330451875543 -0.42395679691615
   C 1.2579793305529 0.10253815475833 0.20100853006798
   O 0.07157373218152 -1.42176383766864 -1.19973295254716
   H -1.22116019071807 1.21731682582838 -0.14125628889309
   H -1.4330436431626 -0.04892803967934 1.06432799065161
   H -2.10110516465872 -0.27062142792271 -0.56236052059465
   H 1.38126815602784 1.12055904935252 -0.16250100941439
   H 2.13759306261 -0.4780527025027 -0.06252115184424
   H 1.15199798147051 0.14140874232516 1.28222772425865
   
   $ leruli graph-to-formula "CC(=O)C"
   C3H6O


Examples for usage in Python
----------------------------
Load the library

.. code-block:: python

   >>> import leruli

Get a SMILES string from a molecule name.

.. code-block:: 

   >>> leruli.name_to_graph("acetone")
   {'graph': 'CC(=O)C', 'reference': 'wikidata'}

Get a geometry for given molecular graph.

.. code-block:: 

   >>> print(leruli.graph_to_geometry('CC(=O)C', "XYZ")['geometry'])
   10
   Generated with https://api.leruli.com/latest/references/BCE2020,BEG2019,rdkit/bibtex
   C -1.27026192165113 0.14084775426444 0.00476447523142
   C 0.02515865734774 -0.50330451875543 -0.42395679691615
   C 1.2579793305529 0.10253815475833 0.20100853006798
   O 0.07157373218152 -1.42176383766864 -1.19973295254716
   H -1.22116019071807 1.21731682582838 -0.14125628889309
   H -1.4330436431626 -0.04892803967934 1.06432799065161
   H -2.10110516465872 -0.27062142792271 -0.56236052059465
   H 1.38126815602784 1.12055904935252 -0.16250100941439
   H 2.13759306261 -0.4780527025027 -0.06252115184424
   H 1.15199798147051 0.14140874232516 1.28222772425865

Get the sum formula from a molecular graph.

.. code-block:: 
   
   >>> leruli.graph_to_formula("CC=O")
   {'formula': 'C2H4O', 'reference': 'M2013,rdkit'}
