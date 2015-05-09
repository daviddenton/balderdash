#!/bin/sh

export version=$1

git tag -a $version -m "released version $version to PyPi"
git tag
git push origin $version

python setup.py sdist
python setup.py bdist_wheel
