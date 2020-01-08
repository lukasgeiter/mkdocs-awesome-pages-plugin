#!/bin/bash

set -e


if ! git config --get user.name; then
    git config --global user.name "${GITHUB_ACTOR}"
fi

if ! git config --get user.email; then
    git config --global user.email "${GITHUB_ACTOR}@users.noreply.github.com"
fi

git remote rm origin
git remote add origin "https://${GITHUB_ACTOR}:${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"

mkdocs gh-deploy --config-file "${GITHUB_WORKSPACE}/mkdocs.yml" --force