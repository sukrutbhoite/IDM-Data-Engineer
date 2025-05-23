# Code for ETL operations on Country-GDP data

# Importing the required libraries
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import sqlite3
from datetime import datetime


def log_progress(message):
    ''' This function logs the mentioned message of a given stage of the
    code execution to a log file. Function returns nothing'''

    timestamp_format = '%Y-%h-%d-%H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)

    with open(log_file,'a+') as file:
        file.write(f"{timestamp} : {message}\n")


def extract(url, table_attribs):
    ''' This function aims to extract the required
    information from the website and save it to a data frame. The
    function returns the data frame for further processing. '''

    html_data = requests.get(url).text
    data = BeautifulSoup(html_data, 'html.parser')

    tables = data.find_all('tbody')
    rows = tables[0].find_all('tr')

    df = pd.DataFrame(columns=table_attribs)
    for row in rows:
        col = row.find_all('td')
        if len(col) != 0:

            data_dict = {"Name" : str(col[1].find_all('a')[1].contents[0]),"MC_USD_Billion" : float(col[2].contents[0])}

            df = pd.concat([df, pd.DataFrame(data_dict, index = [0])], ignore_index = True)

    print(df)
    return df

def transform(df, csv_path):
    ''' This function accesses the CSV file for exchange rate
    information, and adds three columns to the data frame, each
    containing the transformed version of Market Cap column to
    respective currencies'''

    df1 = pd.read_csv(csv_path)
    exchange_rate = df1.set_index('Currency')['Rate'].to_dict()

    df['MC_EUR_Billion'] = [np.round(x * exchange_rate['EUR'], 2) for x in df['MC_USD_Billion']]
    df['MC_GBP_Billion'] = [np.round(x * exchange_rate['GBP'], 2) for x in df['MC_USD_Billion']]
    df['MC_INR_Billion'] = [np.round(x * exchange_rate['INR'], 2) for x in df['MC_USD_Billion']]

    print(df)
    return df

def load_to_csv(df, output_path):
    ''' This function saves the final data frame as a CSV file in
    the provided path. Function returns nothing.'''

    df.to_csv(output_path, index = False)

def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final data frame to a database
    table with the provided name. Function returns nothing.'''

    df.to_sql(table_name, sql_connection, if_exists='replace')

def run_query(query_statement, sql_connection):
    ''' This function runs the query on the database table and
    prints the output on the terminal. Function returns nothing. '''

    print(pd.read_sql(query_statement, sql_connection))



''' Here, you define the required entities and call the relevant
functions in the correct order to complete the project. Note that this
portion is not inside any function.'''

code_name = 'banks_project.py'
url = 'https://web.archive.org/web/20230908091635 /https://en.wikipedia.org/wiki/List_of_largest_banks'
exchange_rate_csv	= 'exchange_rate.csv'
table_attributes_initial = ['Name', 'MC_USD_Billion']
table_attributes_final = ['Name', 'MC_USD_Billion', 'MC_GBP_Billion', 'MC_EUR_Billion', 'MC_INR_Billion']
output_csv_path = './Largest_banks_data.csv'
database_name = 'Banks.db'
table_name = 'Largest_banks'
log_file = 'code_log.txt'
pd.set_option('display.max_columns', None)

log_progress('Preliminaries complete. Initiating ETL process')

extracted_data = extract(url, table_attributes_initial)
log_progress('Data extraction complete. Initiating Transformation process')

transformed_date = transform(extracted_data, exchange_rate_csv)
log_progress('Data transformation complete. Initiating Loading process')

load_to_csv(transformed_date, output_csv_path)
log_progress('Data saved to CSV file')

sql_connection = sqlite3.connect(database_name)
log_progress('SQL Connection initiated')

load_to_db(transformed_date, sql_connection, table_name)
log_progress('Data loaded to Database as a table, Executing queries')

run_query(query_statement = f"SELECT * FROM {table_name}", sql_connection = sql_connection)
run_query(query_statement = f"SELECT AVG(MC_GBP_Billion) FROM {table_name}", sql_connection = sql_connection)
run_query(query_statement = f"SELECT Name from {table_name} LIMIT 5", sql_connection = sql_connection)
log_progress('Process Complete')

sql_connection.close()
log_progress('Connection closed')