import glob
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime


log_file = "log_file.txt"
target_file = "transformed_data.csv"


def extract():
    initial_dataframe = pd.DataFrame()
    files = glob.glob("*")

    for file in files:
        if file.endswith(".csv") and not file.startswith("transformed"):
            initial_dataframe = pd.concat([initial_dataframe, pd.read_csv(file)], ignore_index=True)
        if file.endswith(".xml"):
            initial_dataframe = pd.concat([initial_dataframe, pd.read_xml(file)], ignore_index=True)
        if file.endswith(".json"):
            initial_dataframe = pd.concat([initial_dataframe, pd.read_json(file, lines=True)], ignore_index=True)

    return initial_dataframe


def transform(data):
    data["height"] = round(data.height * 0.0254,2)
    data['weight'] = round(data.weight * 0.45359237, 2)

    return data

def load_data(target_file, transformed_data):
    transformed_data.to_csv(target_file)

def log_progress(message):
    timestamp_format = '%Y-%h-%d-%H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)

    with open(log_file, 'a+') as file:
        file.write(timestamp + " " + message + "\n")

def main():
    # Log the initialization of the ETL process
    log_progress("ETL Job Started")

    # Log the beginning of the Extraction process
    log_progress("Extract phase Started")
    extracted_data = extract()

    # Log the completion of the Extraction process
    log_progress("Extract phase Ended")

    # Log the beginning of the Transformation process
    log_progress("Transform phase Started")
    transformed_data = transform(extracted_data)
    print("Transformed Data")
    print(transformed_data)

    # Log the completion of the Transformation process
    log_progress("Transform phase Ended")

    # Log the beginning of the Loading process
    log_progress("Load phase Started")
    load_data(target_file, transformed_data)

    # Log the completion of the Loading process
    log_progress("Load phase Ended")

    # Log the completion of the ETL process
    log_progress("ETL Job Ended")


if __name__ == "__main__":
    main()