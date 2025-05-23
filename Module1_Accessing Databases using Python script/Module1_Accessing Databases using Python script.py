import sqlite3
import pandas as pd


db_name = "Staff.db"
table_name = 'Instructor'

with sqlite3.connect(db_name) as conn:

    df = pd.read_csv("INSTRUCTOR.csv", names=['ID', 'FNAME', 'LNAME', 'CITY', 'CCODE']).set_index('ID')
    df.to_sql(table_name, conn, if_exists = 'replace')

    print(pd.read_sql(f"SELECT * FROM {table_name}", conn))

    print(pd.read_sql(f"SELECT COUNT(*) AS Total FROM {table_name}", conn))

    data_dict = {'ID': [100], 'FNAME': ['John'], 'LNAME': ['Doe'], 'CITY': ['Paris'], 'CCODE': ['FR']}

    pd.DataFrame(data_dict).to_sql(table_name, conn, if_exists='append', index=False)
    print('Data appended successfully')

    print(pd.read_sql(f"SELECT * FROM {table_name}", conn))

    print(pd.read_sql(f"SELECT COUNT(*) AS Total FROM {table_name}", conn))