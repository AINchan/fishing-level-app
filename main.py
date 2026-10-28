import os
import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

app = FastAPI()

def get_connection():
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=5432,
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/methods")
def get_methods():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, multiplier FROM methods")
            rows = cur.fetchall()

    methods = []
    for row in rows:
        methods.append({"id": row[0], "name": row[1], "multiplier": float(row[2])})
    return methods

@app.get("/species")
def get_species(min_rank: int = 1):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, rank FROM species WHERE rank >= %s",(min_rank,))
            rows = cur.fetchall()

    species = []
    for row in rows:
        species.append({"id": row[0], "name": row[1], "rank": row[2]})
    return species