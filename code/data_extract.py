import requests
import pandas as pd
from datetime import datetime
import sys

sys.path = [
  "/home/abhishek/Documents/Study/dmml_assignment/group_4_dmml",
]
from config import LAKE_DIR, RAW_SOURCE_DIR

def run_ingestion():
    """Function to be called by Airflow PythonOperator"""
    # Simulate fetching interaction data from a source
    interaction_data_path = RAW_SOURCE_DIR / "interactions_dirty.csv"
    user_data_path = RAW_SOURCE_DIR / "users_dirty.csv"
    
    # Read interaction data
    interactions_df = pd.read_csv(interaction_data_path)
    users_df = pd.read_csv(user_data_path)
    
    # Standard Data Lake naming convention
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    interaction_file_name = f"interactions_{timestamp}.csv"
    user_file_name = f"users_{timestamp}.csv"

    year = datetime.now().strftime("%Y")
    month = datetime.now().strftime("%m")
    day = datetime.now().strftime("%d")

    interaction_full_path = LAKE_DIR / "interaction" / f"year={year}" / f"month={month}" / f"day={day}" / interaction_file_name
    user_full_path = LAKE_DIR / "users" / f"year={year}" / f"month={month}" / f"day={day}" / user_file_name
    interaction_full_path.parent.mkdir(parents=True, exist_ok=True)
    user_full_path.parent.mkdir(parents=True, exist_ok=True)

    # Save the data
    interactions_df.to_csv(interaction_full_path, header=True, index=False)
    users_df.to_csv(user_full_path, header=True, index=False)

    return str(interaction_full_path), str(user_full_path)

#test
if __name__ == "__main__":
    saved_path = run_ingestion()
    print(f"Data saved to: {saved_path}")