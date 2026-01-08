from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging

# ------------------------
# Task functions
# ------------------------

def ingest_data():
    logging.info("Ingesting data from CSV and REST API")

def transform_data():
    logging.info("Transforming and cleaning data")

def train_model():
    logging.info("Training recommendation model")

# ------------------------
# DAG definition
# ------------------------

with DAG(
    dag_id="reco_data_pipeline",
    description="End-to-end recommendation data pipeline",
    start_date=datetime(2026, 1, 1),   # explicit start_date (required in Airflow 3.x)
    schedule=timedelta(days=1),        # daily run
    catchup=False,
    tags=["reco", "dmml", "assignment"],
) as dag:

    ingest = PythonOperator(
        task_id="ingest_data",
        python_callable=ingest_data,
    )

    transform = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data,
    )

    train = PythonOperator(
        task_id="train_model",
        python_callable=train_model,
    )

    ingest >> transform >> train


#Plan schedule 
1. code/rest_api_setup.py : Sets up a FastAPI server to upload and retrieve product data via REST API.
2. code/api_data_extract.py : Fetches product data from the REST API and saves it
3. code/data_extract.py : for interaction and users data into datalake
4. 