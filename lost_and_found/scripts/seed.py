# モックデータ挿入スクリプト
import os
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://app:app@localhost:5432/app")

def parse_pg_url(url):
    # postgresql://user:pass@host:port/db
    import re
    m = re.match(r"postgresql(?:\+.+)?://([^:]+):([^@]+)@([^:/]+):?(\d+)?/([^?]+)", url)
    if not m:
        raise ValueError("Invalid DATABASE_URL")
    user, password, host, port, db = m.groups()
    return dict(user=user, password=password, host=host, port=int(port or 5432), dbname=db)

pg = parse_pg_url(DATABASE_URL)
conn = psycopg2.connect(**pg)
cur = conn.cursor()

cur.execute(
    "INSERT INTO users (id, username, password_hash, role) VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING",
    (1, "admin", "$2b$12$dummyhash", "admin"),
)
cur.execute(
    "INSERT INTO items (id, management_number, found_datetime, found_place, category_l, status) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING",
    (1, "MNG-0001", datetime.now(), "駅前", "財布", "保管中"),
)
conn.commit()
cur.close()
conn.close()
