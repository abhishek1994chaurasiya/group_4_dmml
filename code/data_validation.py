import glob
import pandas as pd
from pathlib import Path
import sys
import great_expectations as gx
sys.path = [
  "/home/abhishek/Documents/Study/dmml_assignment/group_4_dmml",
]
from config import REPORT_DIR, USER_INTERACTION_DIR

# REPORT_DIR = Path("../data/analytics")

REPORT_DIR.mkdir(parents=True, exist_ok=True)
from datetime import datetime
year = datetime.now().strftime("%Y")
month = datetime.now().strftime("%m")
day = datetime.now().strftime("%d")
# day=10
interaction_search_dir = USER_INTERACTION_DIR / f"year={year}" / f"month={month}" / f"day={day}"

def validate_interactions(interaction_search_dir: str):
    files = list(interaction_search_dir.glob("interactions*.csv"))
    if not files:
        raise FileNotFoundError(f"No interaction files found in {interaction_search_dir}")
    
    df_list = [pd.read_csv(f) for f in files]
    df = pd.concat(df_list, ignore_index=True)

    context = gx.get_context()
    data_source = context.data_sources.add_pandas("pandas")
    data_asset = data_source.add_dataframe_asset(name="pd dataframe asset")
    batch_definition = data_asset.add_batch_definition_whole_dataframe("batch definition")
    batch = batch_definition.get_batch(batch_parameters={"dataframe": df})
    
    print(batch.head())
    suite_name = "interaction_expectation_suite"
    suite = gx.ExpectationSuite(name=suite_name)
    suite = context.suites.add(suite)

    # Create Expectation.
    #schema mismatch check
    expectation = gx.expectations.ExpectTableColumnsToMatchSet(column_set=[
        "interaction_id","user_id","product_id", "action", "rating", "timestamp","device", "session_duration_sec"
    ])
    suite.add_expectation(expectation)

    #Missing values
    expectation = gx.expectations.ExpectColumnValuesToNotBeNull(column="interaction_id") #It should be primary key else data issue
    suite.add_expectation(expectation)

    expectation = gx.expectations.ExpectColumnValuesToNotBeNull(column="user_id") #make sure user_id is not null as its linked with interaction id
    suite.add_expectation(expectation)

    expectation = gx.expectations.ExpectColumnValuesToNotBeNull(column="product_id") #make sure product_id is not null as its linked with interaction id
    suite.add_expectation(expectation)

    #Range checks

    expectation = gx.expectations.ExpectColumnValuesToBeBetween(
        column="rating",
        min_value=1,
        max_value=5
    )
    suite.add_expectation(expectation)

    expectation = gx.expectations.ExpectColumnValuesToBeBetween(
        column="session_duration_sec",
        min_value=0,
        max_value=3600
    )
    suite.add_expectation(expectation)

    expectation = gx.expectations.ExpectTableRowCountToBeBetween(
        min_value=1000,
        max_value=1000000
    )
    suite.add_expectation(expectation)

    #duplicate entries
    expectation = gx.expectations.ExpectSelectColumnValuesToBeUniqueWithinRecord(          
        column_list=["interaction_id", "user_id", "product_id", "timestamp"]
    )
    suite.add_expectation(expectation)
    
    # Validate Batch using Expectation.
    validation_result = batch.validate(suite)
    print(validation_result)

    report_path = REPORT_DIR / "interaction_data_quality_report.txt"

    with open(report_path, "w") as report_file:
        report_file.write(str(validation_result))
    
    return report_path

# if __name__ == "__main__":
#     validate_interactions("data/datalake/preprocessed/interaction/year=2026/month=01/day=10/interactions_20260110_213116.csv")