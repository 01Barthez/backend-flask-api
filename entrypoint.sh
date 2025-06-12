#!/bin/bash
set -e

# Run database migrations
flask db upgrade

# Start the application
exec gunicorn --bind 0.0.0.0:5000 src.app.main:create_app()
