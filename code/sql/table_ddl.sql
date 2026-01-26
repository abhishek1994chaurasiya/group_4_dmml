--------------------------------TABLE DDL FOR RECOMART DATABASE---------------------------------
CREATE DATABASE IF NOT EXISTS recomart;

CREATE DATABASE IF NOT EXISTS recomart_transformed;

USE recomart;

--------------------------------TABLE DDL TABLE---------------------------------
DROP TABLE IF EXISTS user_interactions;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS USERS;

CREATE EXTERNAL TABLE IF NOT EXISTS user_interactions (
    interaction_id STRING,
    user_id STRING,
    product_id STRING,
    rating float,
    event_timestamp TIMESTAMP,
    session_duration_sec FLOAT,
    is_action_click BOOLEAN,
    is_action_invalid_data BOOLEAN,
    is_action_purchase BOOLEAN,
    is_action_view BOOLEAN,
    is_device_invalid_data BOOLEAN,
    is_device_mobile BOOLEAN,
    is_device_tablet BOOLEAN,
    sys_unix_timestamp FLOAT
)
USING csv
OPTIONS (
    path '/home/abhishek/Documents/Study/dmml_assignment/group_4_dmml/data/datalake/processed/interaction/',
    header 'true'
);


CREATE EXTERNAL TABLE IF NOT EXISTS products (
    product_id STRING,
    product_name STRING,
    brand STRING,
    price FLOAT,
    rating FLOAT,
    stock_level FLOAT,
    is_category_Electronics BOOLEAN,
    is_category_Fashion BOOLEAN,
    is_category_Home BOOLEAN,
    is_category_Sports BOOLEAN
)
USING csv
OPTIONS (
    path '/home/abhishek/Documents/Study/dmml_assignment/group_4_dmml/data/datalake/processed/products/',
    header 'true',
    quote '"',
    escape '"'
);
CREATE EXTERNAL TABLE IF NOT EXISTS USERS (
    user_id STRING,
    user_name STRING,
    email STRING,
    age FLOAT,
    city STRING,
    signup_date DATE,
    is_gender_invalid_data BOOLEAN,
    is_male BOOLEAN,
    gender_other Boolean
) USING csv
OPTIONS (
    path '/home/abhishek/Documents/Study/dmml_assignment/group_4_dmml/data/datalake/processed/users/',
    header 'true',
    quote '"',
    escape '"'
);

--------
use recomart_transformed;

DROP TABLE IF EXISTS user_activity_frequency;
DROP TABLE IF EXISTS user_average_rating;
DROP TABLE IF EXISTS item_avg_rating;
DROP TABLE IF EXISTS item_cooccurrence;

--------------------------------TABLE DDL FOR TRANSFORMED FEATURES---------------------------------
--user activity frequency
CREATE TABLE user_activity_frequency (
  user_id STRING,
  total_interactions BIGINT NOT NULL)
USING DELTA;

--average rating per user
CREATE TABLE user_average_rating (
  user_id STRING,
  average_rating DOUBLE)
USING DELTA;

--average rating per item
CREATE TABLE item_avg_rating (
  product_id STRING,
  avg_item_rating DOUBLE,
  rating_count BIGINT NOT NULL)
USING DELTA;

--co-occurrence / similarity-based features
CREATE TABLE item_cooccurrence (
    product_id_1 STRING,
    product_id_2 STRING,
    co_occurrence_count BIGINT NOT NULL)
USING DELTA;
