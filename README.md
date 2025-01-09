# Repository to host the Python documentation for OPM Flow

## Building the documentation locally
Follow the commands in `.github/workflows/python_sphinx_docs.yml` for your local setup!

See also the script [opmdoc-download-files](https://github.com/OPM/opm-python-documentation/blob/master/python/sphinx_docs/README.md) for more information.

## Building the documentation online on your fork
- Turn on github actions at `https://github.com/<your-github-username>/opm-python-documentation/actions`
- Push any changes to a branch of your fork, this should trigger a build of the documentation, where the built documentation is pushed to the branch `gh-pages-<name-of-your-branch>`
- Then you can turn on github pages for your fork at `https://github.com/<your-github-username>/opm-python-documentation/settings/pages`
- Select the branch `gh-pages-<name-of-your-branch>` as the source for your github page
- Then you can have a look at the documentation with your changes at `https://<your-github-username>.github.io/opm-python-documentation/<name-of-your-branch>/index.html`
- If everything looks fine, create a pull request for the master branch of this repository :)
