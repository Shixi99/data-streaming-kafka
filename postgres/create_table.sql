CREATE TABLE sentences (
    id SERIAL PRIMARY KEY,
    sentence VARCHAR(1000) NOT NULL,
    sentiment FLOAT
)