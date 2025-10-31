CREATE TABLE edges (
    osmid SERIAL PRIMARY KEY,
    u integer REFERENCES nodes (osmid),
    v integer REFERENCES nodes (osmid),
    CHECK ( u <> v ),
    highway VARCHAR (255),
    maxspeed integer,
    name VARCHAR (255),
    oneway BOOLEAN DEFAULT FALSE,
    reversed BOOLEAN,
    length FLOAT,
    geom GEOMETRY(LINESTRING, 4326)
);