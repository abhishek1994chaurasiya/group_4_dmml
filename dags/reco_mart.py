#############################################################
# DAG: reco_data_pipeline
# Description: End-to-end recommendation data pipeline
# Schedule: Daily
# Pre-requisites:
#   - FastAPI server running on port 9000 (code/rest_api_setup.py)
#   - MLflow server running on port 5000
#############################################################

from pathlib import Path
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import logging
from airflow.utils.task_group import TaskGroup
import requests
import papermill as pm


code_path='/home/abhishek/Documents/Study/dmml_assignment/group_4_dmml/code/'
raw_data_path='/home/abhishek/Documents/Study/dmml_assignment/group_4_dmml/data/source_raw/'


# ------------------------
# Task functions
# ------------------------

OUTPUT_DIR = Path("/tmp/notebook_outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def run_notebook(**context):
    output_path = OUTPUT_DIR / f"train_model_{context['ds_nodash']}.ipynb"
    pm.execute_notebook(
        input_path=code_path +'SampleDataGenerator_v2.ipynb',
        output_path=str(output_path),
        parameters={
            "run_date": context["ds"],
        #     "input_path": "/data/input/"
        }
    )
def post_data_function():
    logging.info("Posting product data to REST API")
    requests.post(
        "http://127.0.0.1:9000/upload-dataset",
        files={"file": open(raw_data_path + "products_dirty.csv", "rb")}
    )

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

    with TaskGroup(group_id="dataops_prework") as ingestion_group:
        data_gen = PythonOperator(
            task_id="data_generator_notebook",
            python_callable=run_notebook,
        )

        upload_task = PythonOperator(
            task_id="post_product_data",
            python_callable=post_data_function,
        )

        data_gen >> upload_task


    api_extract = BashOperator(
        task_id="api_data_extract",
        bash_command="python "+code_path+"api_data_extract.py",
    )
    csv_extract = BashOperator(
        task_id="csv_data_extract",
        bash_command="python "+code_path+"data_extract.py",
    )
    data_validation_profiling = BashOperator(
        task_id="data_validation_interaction_data",
        bash_command="python "+code_path+"data_validation.py",
    )
    feature_engineering = BashOperator(
        task_id="feature_engineering",
        bash_command="bash "+code_path+"06_FE_and_transformation.sh",
    )


    ingest = ingestion_group >> [api_extract, csv_extract] >> data_validation_profiling
    data_validation_profiling >> feature_engineering





#     transform = PythonOperator(
#         task_id="transform_data",
#         python_callable=transform_data,
#     )

#     train = PythonOperator(
#         task_id="train_model",
#         python_callable=train_model,
#     )

#     ingest >> transform >> train


# #Plan schedule 
# 1. code/rest_api_setup.py : Sets up a FastAPI server to upload and retrieve product data via REST API.
# 2. code/api_data_extract.py : Fetches product data from the REST API and saves it
# 3. code/data_extract.py : for interaction and users data into datalake
# 4. 