#!/bin/sh

#run tests here!

export VERSION=$1

git tag -a $version -m "released version $version to PyPi"
git tag
git push origin $version

python setup.py sdist upload -r pypi
python setup.py bdist_wheel upload -r pypi
