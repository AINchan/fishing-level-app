import os
import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI
from typing import Literal
from pydantic import BaseModel

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
            cur.execute("SELECT id, name, default_multiplier, fishing_area FROM methods")
            rows = cur.fetchall()

    methods = []
    for row in rows:
        methods.append({"id": row[0], "name": row[1], "default_multiplier": float(row[2]), "fishing_area": row[3]})
    return methods

@app.get("/species")
def get_species(min_rank: int = 1):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, measure_type, rank FROM species WHERE rank >= %s",(min_rank,))
            rows = cur.fetchall()

    species = []
    for row in rows:
        species.append({"id": row[0], "name": row[1], "measure_type": row[2], "rank": row[3]})
    return species


class TripCreate(BaseModel):
    latitude: float
    longitude: float
    fishing_area: Literal["shore", "offshore"]

@app.post("/trips")
def create_trip(trip: TripCreate):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO trips (user_id, latitude, longitude, fishing_area) "
                "VALUES (%s, %s, %s, %s) RETURNING id, start_at, status",
                (1, trip.latitude, trip.longitude, trip.fishing_area),
            )
            row = cur.fetchone()

    return {"id": row[0], "start_at": row[1], "status": row[2]}


class CatchCreate(BaseModel):
    species_id: int
    method_id: int    
    length: float | None = None
    weight: int | None = None
    finger: float | None = None
    

@app.post("/trips/{trip_id}/catches")
def create_catches(trip_id: int, catch: CatchCreate):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO catches (trip_id, species_id, method_id, length_cm, weight_g, finger_count)"
                "VALUES (%s,%s,%s,%s,%s,%s) RETURNING id",
                (trip_id, catch.species_id, catch.method_id, catch.length, catch.weight, catch.finger),
            )
            row = cur.fetchone()

    return {"id": row[0]}