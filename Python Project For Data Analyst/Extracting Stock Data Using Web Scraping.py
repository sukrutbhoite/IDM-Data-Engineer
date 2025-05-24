import pandas
import pandas as pd
from bs4 import BeautifulSoup
import requests


def using_BeautifulSoup(url):
    html_page = requests.get(url).text
    html_data = BeautifulSoup(html_page, 'html.parser')
    table_data = html_data.find_all('tbody')
    rows = table_data[0].find_all('tr')


    df = pd.DataFrame()
    for row in rows:

        cols = row.find_all('td')
        data_dict = {"Date"      : cols[0].text,
                     "Open"      : cols[1].text,
                     "High"      : cols[2].text,
                     "Low"       : cols[3].text,
                     "Close"     : cols[4].text,
                     "Adj Close" : cols[5].text,
                     "Volume"    : cols[6].text}

        df = pd.concat([df, pd.DataFrame(data_dict, index = [0])], ignore_index = True)

    return df.set_index("Date")


def using_Pandas(url):
    df = pd.read_html(url)[0]

    return df.set_index("Date")


def main():
    url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/netflix_data_webpage.html"

    df1 = using_BeautifulSoup(url)
    df2 = using_Pandas(url)

    print("Using BeautifulSoup:")
    print(df1.head())
    print("Using Pandas:")
    print(df2.head())

if __name__ == "__main__":
    main()
