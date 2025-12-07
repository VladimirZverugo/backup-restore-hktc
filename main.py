import os
import sys
import json
import base64
import gzip
import subprocess
import psycopg2
import requests


def need(name): 
    v = os.getenv(name)
    if not v:
        print(f"{name} not set", file=sys.stderr)
        sys.exit(1)
    return v


def fetch_dump(base_url, token):
    r = requests.get( 
        f"{base_url}/challenges/backup_restore/problem",
        params={"access_token": token}, 
    )
    r.raise_for_status()
    return base64.b64decode(r.json()["dump"])


def restore_dump(dump_bytes, db_url):
    sql = gzip.decompress(dump_bytes)
    subprocess.run(
        ["psql", db_url], 
        input=sql,
        check=True
    )


def get_alive(db_url): 
    conn = psycopg2.connect(db_url)
    try:
        cur = conn.cursor()
        cur.execute("SELECT ssn FROM criminal_records WHERE status = 'alive'")
        return [row[0] for row in cur.fetchall()]
    finally:
        conn.close()


def submit(base_url, token, ssns): 
    r = requests.post(
        f"{base_url}/challenges/backup_restore/solve",
        params={"access_token": token}, 
        json={"alive_ssns": ssns},
    )
    r.raise_for_status()
    return r.json()


def main(): 
    base_url = os.getenv("BASE_URL")
    token = need("ACCESS_TOKEN")
    db_url = need("DATABASE_URL")

    dump_bytes = fetch_dump(base_url, token)
    restore_dump(dump_bytes, db_url)
    alive = get_alive(db_url)
    print(json.dumps(submit(base_url, token, alive), indent=2))


if __name__ == "__main__":
    main()
