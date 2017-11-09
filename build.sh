#!/bin/bash

echo 'Creating deployment zip...'

git archive -o deploy.zip HEAD

echo 'Done.'
