CREATE TABLE nodes (
    osmid SERIAL PRIMARY KEY,
    x FLOAT,
    y FLOAT,
    highway VARCHAR (255)
);