#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install requirements and dependencies
pip install -r requirements.txt

# Collect and store static asset files
python manage.py collectstatic --no-input

# Apply any database migrations
python manage.py migrate