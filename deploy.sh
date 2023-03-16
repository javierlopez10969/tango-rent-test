#!/usr/bin/env sh

# abort on errors
set -e

# folder select
cd frontend

# build
npm run build

# navigate into the build output directory
cd dist

git init
git add -A
git commit -m 'deploy'

# if you are deploying to https://<USERNAME>.github.io/<REPO>
git push -f https://github.com/javierlopez10969/fullstack-test-tango/.git main:gh-pages

cd -