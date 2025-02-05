#!/bin/bash

# Wait for the database to be ready
# echo "Waiting for database..."
# while ! nc -z db 5432; do
#   sleep 1
# done
# echo "Database is up!"

# Run migrations
echo "Running migrations..."
flask db upgrade

# # Optionally run seeds
if [ "$FLASK_ENV" = "development" ]; then
  echo "Running seeds..."
  python ./seeds/seeds_brands_sizes.py
fi

# Start the Flask app
echo "Starting Flask app..."
exec "$@"
