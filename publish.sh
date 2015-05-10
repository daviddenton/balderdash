#!/bin/sh

export VERSION=$1

python setup.py test

git tag -a $VERSION -m "released version $VERSION to PyPi"
git tag
git push origin $VERSION

python setup.py sdist upload -r pypi
python setup.py bdist_wheel upload -r pypi
