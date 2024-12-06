CREATE TABLE IF NOT EXISTS smart_fridge_data (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    temperature VARCHAR(10),
    threshold DECIMAL(5, 2),
    bottle_number INT,
    heating_element INT
);