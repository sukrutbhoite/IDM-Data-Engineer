import pandas as pd
from bs4 import BeautifulSoup
import requests
import sqlite3


def average_rank(rows, count = 50):
    df = pd.DataFrame()

    for rank,row in enumerate(rows):

        if rank <= count:
            col = row.find_all('td')

            if len(col) != 0:

                data_dict = {"Average Rank" : col[0].contents[0], "Film" : col[1].contents[0], "Year" : col[2].contents[0]}

                df = pd.concat([df,pd.DataFrame(data_dict, index=[0])], ignore_index=True)

        else:
            break

    return df.set_index("Average Rank")


def rotten_tomatoes(rows, count = 50):
    df = pd.DataFrame()

    for rank, row in enumerate(rows):

        if rank <= count:
            col = row.find_all('td')

            if len(col) != 0:

                data_dict = {"Film": col[1].contents[0], "Year": col[2].contents[0], "Rotten Tomatoes" : col[3].contents[0]}

                df = pd.concat([df, pd.DataFrame(data_dict, index=[0])], ignore_index=True)

        else:
            break

    return df.set_index("Film")


def write(df, csv_path = "temp.csv", db_name = "Temp.db", table_name = "temp"):
    df.to_csv(csv_path)

    with sqlite3.connect(db_name) as conn:
        df.to_sql(table_name, conn, if_exists = "replace")

def main():
    url = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'

    html_page = requests.get(url).text
    data = BeautifulSoup(html_page, 'html.parser')
    tables = data.find_all('tbody')
    rows = tables[0].find_all('tr')


    write(average_rank(rows), 'top_50_films_by_rank.csv', 'Movies_By_Rank.db', 'Top_50')
    write(rotten_tomatoes(rows), 'top_50_films_by_rotten_tomatoes.csv', 'Movies_By_Rotten_Tomatoes.db', 'Top_50')

if __name__ == "__main__":
    main()