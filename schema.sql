DROP TABLE IF EXISTS catches;
DROP TABLE IF EXISTS trip_methods;
DROP TABLE IF EXISTS trips;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS methods;
DROP TABLE IF EXISTS species;
DROP TABLE IF EXISTS ranks;
DROP TABLE IF EXISTS genres;

CREATE TABLE genres (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE ranks (
    rank INTEGER PRIMARY KEY,
    base_xp INTEGER NOT NULL
);

CREATE TABLE species (
    id SERIAL PRIMARY KEY,
    name TEXT NOT null UNIQUE,
    genre_id INTEGER NOT null REFERENCES genres(id),
    rank INTEGER NOT null REFERENCES ranks(rank),
    water_type TEXT NOT NULL CHECK (water_type IN ('salt', 'fresh')),
    standard_size NUMERIC(7, 1) NOT NULL,
    measure_type TEXT NOT NULL CHECK (measure_type IN ('length', 'weight', 'finger')),
    good_size NUMERIC(7, 1) NOT NULL,
    lunker_size NUMERIC(7, 1) NOT NULL,
    record_size NUMERIC(7, 1) NOT NULL,
    CHECK (good_size < lunker_size AND lunker_size < record_size)
);

CREATE TABLE methods (
    id SERIAL PRIMARY KEY,
    name TEXT NOT null UNIQUE,
    default_multiplier NUMERIC(2,1) NOT NULL,
    fishing_area TEXT NOT null CHECK (fishing_area IN ('shore', 'offshore', 'both'))
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    display_name TEXT NOT NULL,
    start_level INTEGER NOT NULL DEFAULT 1,
    estimated_level INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE trips(
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT null REFERENCES users(id) ON DELETE CASCADE,
    start_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    end_at TIMESTAMPTZ,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    fishing_area TEXT NOT null CHECK (fishing_area IN ('shore', 'offshore')),
    status TEXT NOT null DEFAULT 'in_progress' CHECK (status IN ('in_progress','provisional','confirmed'))
);

CREATE TABLE trip_methods(
    id SERIAL PRIMARY KEY,
    trip_id INTEGER NOT null REFERENCES trips(id) ON DELETE CASCADE,
    method_id INTEGER NOT null REFERENCES methods(id),
    UNIQUE (trip_id, method_id)
);

CREATE TABLE catches(
    id SERIAL PRIMARY KEY,
    trip_id INTEGER NOT null REFERENCES trips(id) ON DELETE CASCADE,
    species_id INTEGER NOT null REFERENCES species(id),
    method_id INTEGER NOT null REFERENCES methods(id),
    length_cm NUMERIC(4,1),
    weight_g INTEGER,
    finger_count NUMERIC(2,1),
    photo_path TEXT,
    photo_taken_at TIMESTAMPTZ,
    photo_hash TEXT,
    is_verified BOOLEAN NOT null DEFAULT false
);