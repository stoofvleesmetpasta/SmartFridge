CREATE TABLE IF NOT EXISTS smart_fridge_data (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    temperature INT,
    bottle_number INT,
    heating_element INT
);