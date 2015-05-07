#!/bin/sh

$newVersion=$1

git tag -a $newVersion -m "released version $newVersion to PyPi"
git tag
git push origin $newVersion
