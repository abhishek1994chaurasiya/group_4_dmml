--------------------------------TABLE DDL FOR RECOMART DATABASE---------------------------------
CREATE DATABASE IF NOT EXISTS recomart;

CREATE DATABASE IF NOT EXISTS recomart_transformed;

USE recomart;

--------------------------------TABLE DDL TABLE---------------------------------
CREATE TABLE IF NOT EXISTS user_interactions (
    interaction_id STRING,
    user_id STRING,
    product_id STRING,
    action STRING,
    rating FLOAT,
    event_timestamp TIMESTAMP,
    device STRING,
    session_duration_sec FLOAT
)
USING csv
OPTIONS (
    path '/home/abhishek/Documents/Study/dmml_assignment/group_4_dmml/data/datalake/processed/interaction/',
    header 'true'
);


CREATE TABLE IF NOT EXISTS products (
    product_id STRING,
    product_name STRING,
    category STRING,
    brand STRING,
    price FLOAT,
    rating FLOAT,
    stock_level INT
)
USING csv
OPTIONS (
    path '/home/abhishek/Documents/Study/dmml_assignment/group_4_dmml/data/datalake/processed/products/',
    header 'true',
    quote '"',
    escape '"'
);

CREATE TABLE IF NOT EXISTS USERS (
    user_id STRING,
    user_name STRING,
    email STRING,
    gender STRING,
    age INT,
    city STRING,
    signup_date DATE
) USING csv
OPTIONS (
    path '/home/abhishek/Documents/Study/dmml_assignment/group_4_dmml/data/datalake/processed/users/',
    header 'true',
    quote '"',
    escape '"'
);