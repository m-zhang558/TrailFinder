CREATE TABLE nodes (
    osmid SERIAL PRIMARY KEY,
    x FLOAT,
    y FLOAT,
    highway VARCHAR (255),
    geom GEOMETRY(POINT, 4326)
);