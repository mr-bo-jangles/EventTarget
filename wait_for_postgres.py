from time import sleep

import os
import psycopg2

db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT", 5432)
db_name = os.environ.get("DB_NAME")
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASSWORD")

db_waittime = os.environ.get("DB_TIMEOUT", "60")  # Database startup timeout in seconds

for x in range(0, int(db_waittime)):
    try:
        conn = psycopg2.connect(dbname=db_name, host=db_host, port=int(db_port), password=db_pass, user=db_user)
        break
    except Exception:
        print(f"Could not connect to postgres, for {x} seconds")
        sleep(1)
