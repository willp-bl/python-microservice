#!/usr/bin/env bash

set -e

source venv/bin/activate

export FLASK_APP=happ.py
export FLASK_ENV=development

npx webpack
python -m flask run

