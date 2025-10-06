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

# Delete problematic socialaccount migrations
cur.execute("DELETE FROM django_migrations WHERE app='socialaccount';")
conn.commit()

cur.close()
conn.close()

print("Deleted all socialaccount migrations. Now run normal migrate.")
