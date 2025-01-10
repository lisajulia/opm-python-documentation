.PHONY: docs view-docs

CURRENT_BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
GIT_ROOT := $(shell git rev-parse --show-toplevel)

# Build the documentation locally for the current branch
# NOTE: You need to commit your changes before running this command
docs:
	sphinx-versioned -m ${CURRENT_BRANCH} -b ${CURRENT_BRANCH} --git-root ../../

view-docs:
	@xdg-open "file://$(GIT_ROOT)/python/sphinx_docs/docs/_build/$(CURRENT_BRANCH)/index.html"

test:
	pytest tests/

coverage:
	coverage run -m pytest tests
	coverage report -m
