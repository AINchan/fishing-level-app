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
    standard_size NUMERIC(4, 1) NOT NULL,
    measure_type TEXT NOT NULL CHECK (measure_type IN ('length', 'weight', 'finger')),
    good_size NUMERIC(4, 1) NOT NULL,
    lunker_size NUMERIC(4, 1) NOT NULL,
    record_size NUMERIC(4, 1) NOT NULL,
    CHECK (good_size < lunker_size AND lunker_size < record_size)
);

CREATE TABLE methods (
    id SERIAL PRIMARY KEY,
    name TEXT NOT null UNIQUE,
    default_multiplier NUMERIC(2,1) NOT NULL,
    fishing_area TEXT NOT null CHECK (fishing_area IN ('shore', 'offshore', 'both'))
);