# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = python -msphinx
SPHINXPROJ    = leruli
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	find _build/html/ -type f -exec sed -i 's#AAA100AAA#<img alt="Python logo" src="_images/python-brands.png" style="width: 30px;padding-right:0.2em;vertical-align:bottom">Leruli Python package#' {} \;
	find _build/html/ -type f -exec sed -i 's#AAA101AAA#<img alt="Python logo" src="_images/boxes-stacked-solid.png" style="width: 30px;padding-right:0.2em;vertical-align:bottom">Leruli Queue#' {} \;
	find _build/html/ -type f -exec sed -i 's#AAA102AAA#<img alt="Python logo" src="_images/server-solid.png" style="width: 30px;padding-right:0.2em;vertical-align:bottom">Leruli Compute#' {} \;
	find _build/html/ -type f -exec sed -i 's#AAA103AAA#<img alt="Python logo" src="_images/terminal-solid.png" style="width: 30px;padding-right:0.2em;vertical-align:bottom">CLI#' {} \;
