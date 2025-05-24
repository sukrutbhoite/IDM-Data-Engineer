import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)
pio.renderers.default = "iframe"

def make_graph_jupyter(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()
    from IPython.display import display, HTML
    fig_html = fig.to_html()
    display(HTML(fig_html))


def make_graph(stock_data, revenue_data, stock):
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])
    revenue_data['Date'] = pd.to_datetime(revenue_data['Date'])
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=stock_data_specific.Date, y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=revenue_data_specific.Date, y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
                      height=900,
                      title=stock,
                      xaxis_rangeslider_visible=True)
    pio.renderers.default = "browser"
    fig.show()


def using_yfinance(stock):
    ticker = yf.Ticker(stock)
    stock_data = ticker.history(period = 'max')
    stock_data.reset_index(inplace = True)

    return stock_data

def using_BeautifulSoup(url):
    stock_revenue = pd.DataFrame()

    html_data = requests.get(url).text
    soup = BeautifulSoup(html_data, 'html.parser')
    table = soup.find_all('tbody')[1]
    rows = table.find_all('tr')

    for row in rows:
        col = row.find_all('td')
        Date = col[0].contents[0]
        try:
            Revenue = col[1].contents[0]
        except IndexError:
            Revenue = 0
        data_dict = {"Date": Date, "Revenue": Revenue}
        stock_revenue = pd.concat([stock_revenue, pd.DataFrame(data_dict, index=[0])], ignore_index=True)

    stock_revenue["Revenue"] = stock_revenue['Revenue'].str.replace('$',"")
    stock_revenue["Revenue"] = stock_revenue['Revenue'].str.replace(',',"")
    stock_revenue.dropna(inplace=True)
    stock_revenue = stock_revenue[stock_revenue['Revenue'] != ""]

    return stock_revenue

def main():
    tesla_data = using_yfinance("TSLA")
    tesla_revenue = using_BeautifulSoup("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm")

    make_graph(tesla_data, tesla_revenue, "Tesla")

    gme_data = using_yfinance("GME")
    gme_revenue = using_BeautifulSoup('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html')

    make_graph(gme_data, gme_revenue, "GameStop")

if __name__ == "__main__":
    main()