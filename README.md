# Issue importer to GitHub

The aim of this project is to enable issue imports to an empty GitHub repository
retaining issue numbers.

This project uses version 3 of the GitHub API and is licensed under GPL v3 or later.

Be aware that **no** proper **error checking** currently in place.

## Input

Issues from the data directory are imported. Each issue has 2 files encoded in UTF-8:

 - `n.txt` containing the issue body
 - `n.labels` containing the labels line-by-line. If *closed* appears, then issue will be closed.

## Use

 1. install prerequisities
 2. copy `config.sample.json` as `config.json` and fill in the fields there
 3. run `import-issues.py`
 4. enjoy

## Prerequisities

 1. clone this repository
 2. place issues under `data/` as described above
 3. install python and the folowing modules. Package name for Debian/Ubuntu given in parentheses):

     - `requests` (`python-requests`)

 4. acquire a GitHub OAuth token that has write access to the desired repository (choose repo as the scope)
