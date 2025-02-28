#!/usr/bin/env python
import os
import time
import psycopg2

# Database connection parameters from environment variables
dbname = os.environ.get("POSTGRES_DB", "devdatabase")
user = os.environ.get("POSTGRES_USER", "desa")
password = os.environ.get("POSTGRES_PASSWORD", "desa")
host = os.environ.get("POSTGRES_HOST", "database")
port = os.environ.get("POSTGRES_PORT", "5432")

max_retries = 30
retry_interval = 2

# Attempt to connect to the database
for attempt in range(max_retries):
    try:
        print(f"Attempting database connection ({attempt+1}/{max_retries})...")
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.close()
        print("Database connection successful!")
        exit(0)
    except psycopg2.OperationalError as e:
        print(f"Connection attempt failed: {e}")
        if attempt < max_retries - 1:
            print(f"Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
        else:
            print("Maximum retry attempts reached. Could not connect to the database.")
            exit(1) 