#!/bin/sh

export VERSION=$1

if [[ -z "$VERSION" ]]; then
    echo "Usage: $0 <version>"
    exit 1
fi

python setup.py test

git tag -a $VERSION -m "released version $VERSION to PyPi"
git tag
git push origin $VERSION

python setup.py bdist_wheel
twine upload dist/*