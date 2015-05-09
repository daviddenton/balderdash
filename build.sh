#!/bin/sh
set -e

python tests/grafanaTest.py
python tests/kibanaTest.py
