import psycopg2
import os
from urllib.parse import urlparse

url = os.environ.get("DATABASE_URL")
result = urlparse(url)

conn = psycopg2.connect(
    dbname=result.path[1:],
    user=result.username,
    password=result.password,
    host=result.hostname,
    port=result.port
)

cur = conn.cursor()

# Check current migrations
cur.execute("SELECT * FROM django_migrations WHERE app='socialaccount';")
print(cur.fetchall())

cur.execute("SELECT * FROM django_migrations WHERE app='sites';")
print(cur.fetchall())

# Delete problematic migration
cur.execute("DELETE FROM django_migrations WHERE app='socialaccount' AND name='0001_initial';")
conn.commit()

cur.close()
conn.close()

print("Done. Now run: python manage.py migrate sites && python manage.py migrate socialaccount")
