#!/usr/bin/env bash

set -e

export FLASK_APP=happ.py
export FLASK_ENV=development

npx webpack
python -m flask run

