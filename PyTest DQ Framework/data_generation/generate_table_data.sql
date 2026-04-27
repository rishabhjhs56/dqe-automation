-- DDL

DROP TABLE IF EXISTS visits;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS facilities;


CREATE TABLE facilities (
    id SERIAL PRIMARY KEY,
    external_id VARCHAR(50),
    facility_name VARCHAR(100),
    facility_type VARCHAR(50),
    address VARCHAR(200),
    city VARCHAR(50),
    state VARCHAR(50)
);

CREATE  TABLE patients (
    id SERIAL PRIMARY KEY,
    external_id VARCHAR(50),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    address VARCHAR(200),
    date_of_birth DATE
);

CREATE  TABLE visits (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(id),
    facility_id INTEGER REFERENCES facilities(id),
    visit_timestamp TIMESTAMP,
    treatment_cost NUMERIC,
    duration_minutes INTEGER
);

-- DML (Sample Data for 7 days)
INSERT INTO facilities (external_id, facility_name, facility_type, address, city, state)
VALUES
('F001', 'MayoClinic', 'Clinic', '123 Main St', 'Rochester', 'MN'),
('F002', 'City Hospital', 'Hospital', '456 Elm St', 'Minneapolis', 'MN');

INSERT INTO patients (external_id, first_name, last_name, address, date_of_birth)
VALUES
('P001', 'John', 'Doe', '789 Oak St', '1980-01-01'),
('P002', 'Jane', 'Smith', '321 Pine St', '1990-05-15');

-- Visits for last 7 days
INSERT INTO visits (patient_id, facility_id, visit_timestamp, treatment_cost, duration_minutes)
VALUES
(1, 1, '2026-04-18 10:00:00', 150.00, 30),
(2, 2, '2026-04-19 11:00:00', 200.00, 45),
(1, 2, '2026-04-20 09:30:00', 180.00, 35),
(2, 1, '2026-04-21 14:00:00', 160.00, 40),
(1, 1, '2026-04-22 08:00:00', 170.00, 25),
(2, 2, '2026-04-23 15:00:00', 210.00, 50),
(1, 2, '2026-04-24 12:00:00', 190.00, 38);
