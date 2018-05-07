#!/bin/sh

# Wait for the database to be ready.
until /usr/bin/pg_isready -U docker -d docker -h postgres -p 5432; 
do
    sleep 5
done

echo "Now starting the server..."

# Start the server
/usr/bin/python3 -u /src/index.py