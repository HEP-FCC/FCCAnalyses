#!/bin/sh

GH_REPO_ORG=`echo $TRAVIS_REPO_SLUG | cut -d "/" -f 1`
GH_REPO_NAME=`echo $TRAVIS_REPO_SLUG | cut -d "/" -f 2`
GH_REPO_REF="github.com/$GH_REPO_ORG/$GH_REPO_NAME.git"

##### Configure git.
# Set the push default to simple i.e. push only the current branch.
git config --global push.default simple
# Pretend to be an user called Travis CI.
git config user.name "Travis CI"
git config user.email "travis@travis-ci.org"


git clone -b gh-pages https://$GH_TOKEN@github.com/$GH_REPO_ORG/$GH_REPO_NAME.git code_docs
cp -r build/doxygen/html/* code_docs/doc/latest/
cd code_docs
git add --all doc/latest
git commit -m "Deploy code docs to GitHub Pages Travis build: ${TRAVIS_BUILD_NUMBER}" -m "Commit: ${TRAVIS_COMMIT}"
git push origin gh-pages:gh-pages > /dev/null 2>&1
