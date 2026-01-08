import requests
import pandas as pd
from datetime import datetime
import sys

sys.path = [
  "/home/abhishek/Documents/Study/dmml_assignment/group_4_dmml",
]
from config import PRODUCT_DIR, PRODUCT_SOURCE_API_URL

def run_ingestion():
    """Function to be called by Airflow PythonOperator"""
    response = requests.get(PRODUCT_SOURCE_API_URL, timeout=15)
    response.raise_for_status()
    
    data = response.json()
    df = pd.DataFrame(data)
    
    # Standard Data Lake naming convention
    # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    year = datetime.now().strftime("%Y")
    month = datetime.now().strftime("%m")
    day = datetime.now().strftime("%d")

    file_name = f"products.csv"
    full_path = PRODUCT_DIR / f"year={year}" / f"month={month}" / f"day={day}" / file_name
    
    full_path.parent.mkdir(parents=True, exist_ok=True)

    # Save the data
    df.to_csv(full_path, header=True, index=False)
    return str(full_path)

#test
if __name__ == "__main__":
    saved_path = run_ingestion()
    print(f"Data saved to: {saved_path}")