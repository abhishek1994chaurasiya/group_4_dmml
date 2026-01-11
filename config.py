from pathlib import Path

# Directories
BASE_DIR = Path("/home/abhishek/Documents/Study/dmml_assignment/group_4_dmml")
DATA_DIR = BASE_DIR / "data"
LAKE_DIR = DATA_DIR / "datalake"
RAW_API_DIR = DATA_DIR / "source_api_raw/"
RAW_SOURCE_DIR = DATA_DIR / "source_raw/"
PRODUCT_DIR= LAKE_DIR / "preprocessed" / "products/"
USER_INTERACTION_DIR = LAKE_DIR / "preprocessed" / "interaction/"
USERS_DIR = LAKE_DIR / "preprocessed" / "users/"
ANALYTICS_DIR = LAKE_DIR / "analytics/"
REPORT_DIR = BASE_DIR / "reports/"

#API 
PRODUCT_SOURCE_API_URL = "http://127.0.0.1:9000/products"