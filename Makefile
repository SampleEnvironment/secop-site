# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
SPECDIR       = spec
BUILDDIR      = build
BUILDSRCDIR   = buildsrc

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(BUILDSRCDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile rfcs with_spec clone_spec clean_spec

with_spec: Makefile $(BUILDSRCDIR) rfcs
	@$(SPHINXBUILD) -M html "$(BUILDSRCDIR)/$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

$(BUILDSRCDIR): spec
	@cp "secop_sphinx.py" "$(BUILDSRCDIR)"
	@cp -r "$(SOURCEDIR)" "$(BUILDSRCDIR)"
	@cp -r $(BUILDSRCDIR)/spec/protocol/specification/* "$(BUILDSRCDIR)/$(SOURCEDIR)/specification"

rfcs:
	python process_rfcs.py "$(BUILDSRCDIR)/spec/rfcs" "$(BUILDSRCDIR)/$(SOURCEDIR)/rfcs"

spec:
	@if [ ! -d  "$(BUILDSRCDIR)/spec" ]; then \
		git clone "https://github.com/SampleEnvironment/SECoP.git" "$(BUILDSRCDIR)/spec"; \
	fi

clean_spec:
	rm -rf $(BUILDSRCDIR)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
