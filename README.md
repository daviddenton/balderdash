# Balderdash 

[![Build Status](https://api.travis-ci.org/daviddenton/balderdash.svg?branch=master)](https://travis-ci.org/daviddenton/balderdash) [![Coverage Status](https://coveralls.io/repos/daviddenton/balderdash/badge.svg?branch=master)](https://coveralls.io/r/daviddenton/balderdash?branch=master)[![PyPI version](https://badge.fury.io/py/balderdash.svg)](http://badge.fury.io/py/balderdash)

A Python DSL for building various dashboards. Currently supports:
 - Kibana - apply filters and output fields as a table
 - Grafana - multiple rows with multiple (evenly split) panels

## See it:
See the [example code](https://github.com/daviddenton/balderdash/tree/master/examples).

## Get it:
```bash
pip install balderdash
```

## Publish it:
 - Ensure [twine](https://pypi.org/project/twine/) is installed
 - Ensure you've got [~/.pypirc](https://packaging.python.org/specifications/pypirc/) setup with your username
 - If your ~/.pypirc defines your repository as www.python.org/pypi, delete that line. It's wrong.
 - Update version in ./setup.py
 - Run `./publish.sh <version>`
 - Enter your PyPI password (twice)
 - Check it appears on [on PyPI](https://pypi.python.org/pypi/balderdash/)
