import os
import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI
from typing import Literal
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from datetime import datetime

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
            cur.execute("SELECT id FROM trips WHERE user_id = %s AND status = %s", (1, "in_progress"))
            active_trip = cur.fetchone()
            if active_trip is not None:
                raise HTTPException(status_code=409, detail="今の状態と競合している")

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
    length_cm: float | None = None
    weight_g: int | None = None
    finger_count: float | None = None
    

@app.post("/trips/{trip_id}/catches")
def create_catch(trip_id: int, catch: CatchCreate):
    with get_connection() as conn:
        with conn.cursor() as cur:
            
            cur.execute("SELECT id FROM trips WHERE id = %s", (trip_id,))
            trip = cur.fetchone()
            if trip is None:
                raise HTTPException(status_code=404, detail="釣行が見つかりません")

            cur.execute(
                "INSERT INTO catches (trip_id, species_id, method_id, length_cm, weight_g, finger_count)"
                "VALUES (%s,%s,%s,%s,%s,%s) RETURNING id",
                (trip_id, catch.species_id, catch.method_id, catch.length_cm, catch.weight_g, catch.finger_count),
            )
            row = cur.fetchone()

    return {"id": row[0]}


class TripMethodsUpdate(BaseModel):
    method_ids: list[int]

@app.put("/trips/{trip_id}/methods")
def update_trip_methods(trip_id: int, data: TripMethodsUpdate):
    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute("SELECT id FROM trips WHERE id = %s", (trip_id,))
            trip = cur.fetchone()
            if trip is None:
                raise HTTPException(status_code=404, detail="釣行が見つかりません")

            cur.execute("DELETE FROM trip_methods WHERE trip_id = %s", (trip_id,))

            for method_id in data.method_ids:
                cur.execute(
                    "INSERT INTO trip_methods (trip_id, method_id)" 
                    "VALUES (%s,%s)",
                    (trip_id, method_id)
                )
        
    return {"method_ids": data.method_ids}


class TripUpdate(BaseModel):
    end_at: datetime | None = None
    status: Literal["provisional", "confirmed"] | None = None

@app.patch("/trips/{trip_id}")
def update_trip(trip_id: int, data: TripUpdate):
    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute("SELECT id FROM trips WHERE id = %s", (trip_id,))
            trip = cur.fetchone()
            if trip is None:
                raise HTTPException(status_code=404, detail="釣行が見つかりません")

            cur.execute(
                "UPDATE trips "
                "SET end_at = COALESCE(%s, end_at), status = COALESCE(%s,status) "
                "WHERE id = %s "
                "RETURNING id, start_at, end_at, status",
                (data.end_at, data.status, trip_id)
            )

            row = cur.fetchone()
    
    return {"trip_id": row[0], "start_at": row[1], "end_at": row[2], "status": row[3]}
