import os;
import requests;
from datetime import datetime;
from dotenv import load_dotenv;
import numpy as np;
import pandas as pd;
import openpyxl;
import yfinance as yf;
import quandl as quandl;
from utils import *;

load_dotenv("./env/development.env")
quandl.ApiConfig.api_key = os.getenv("QUANDL_API_KEY")

start_date = datetime(2012, 1, 1)
end_date = datetime(2022, 1, 2)
start_string = "2012-01-01"
end_string = "2022-01-01"

spx = yf.Ticker("^GSPC")
spx_1mo_price = spx.history(start=start_date, end=end_date, interval="1mo")
spx_1mo_pct_change = spx_1mo_price.Close.pct_change()[1:]
spx_3mo_price = spx.history(start=start_date, end=end_date, interval="3mo")
spx_3mo_pct_change = spx_3mo_price.Close.pct_change()[1:]
spx_earnings = pd.read_excel("./data/SPX-EARNINGS.xlsx", engine="openpyxl")
spx_earnings = spx_earnings[(spx_earnings["Date"] >= start_string) & (spx_earnings["Date"] <= end_string)]
spx_earnings_pct_change = list(spx_earnings.Value.pct_change()[1:])


ctas = yf.Ticker("CTAS")
ctas_1mo_price = ctas.history(start=start_date, end=end_date, interval="1mo")
ctas_1mo_price.reset_index(inplace=True)
ctas_1mo_price.rename(columns={"index": "Date"}, inplace=True)
ctas_1mo_pct_change = ctas_1mo_price.Close.pct_change()[1:]
ctas_3mo_price = ctas.history(start=start_date, end=end_date, interval="3mo")
ctas_3mo_pct_change = list(ctas_3mo_price.Close.pct_change()[1:])

ctas_obj = getEarnings(
    symbol="CTAS",
)
ctas_earnings = ctas_obj["earnings"]
ctas_earnings_pct_change = ctas_obj["earnings_pct_change"]

aapl_obj = getEarnings(
    symbol="AAPL",
)
aapl_earnings = aapl_obj["earnings"]
aapl_earnings_pct_change = aapl_obj["earnings_pct_change"]

pg_obj = getEarnings(
    symbol="PG",
)
pg_earnings = pg_obj["earnings"]
pg_earnings_pct_change = pg_obj["earnings_pct_change"]

dhi_obj = getEarnings(
    symbol="DHI",
)
dhi_earnings = dhi_obj["earnings"]
dhi_earnings_pct_change = dhi_obj["earnings_pct_change"]

cei = pd.read_csv("./data/USPHCI.csv")
cei_pct_change = periodPctChange(df=cei, key="USPHCI", start_time=start_string, step=1, end_time=end_string)
cei_ctas_pct_change = periodPctChange(df=cei, key="USPHCI", start_time=ctas_earnings["Date"][0], step=3)
cei_aapl_pct_change = periodPctChange(df=cei, key="USPHCI", start_time=aapl_earnings["Date"][0], step=3)
cei_pg_pct_change = periodPctChange(df=cei, key="USPHCI", start_time=pg_earnings["Date"][0], step=3)
cei_dhi_pct_change = periodPctChange(df=cei, key="USPHCI", start_time=dhi_earnings["Date"][0], step=3)

var_spx = np.var(spx_1mo_pct_change)
var_cei = np.var(cei_pct_change)
var_cei_ctas = np.var(cei_ctas_pct_change)
var_cei_aapl = np.var(cei_aapl_pct_change)
var_cei_pg = np.var(cei_pg_pct_change)
var_cei_dhi = np.var(cei_dhi_pct_change)
spx_ctas_cov = np.cov(spx_1mo_pct_change, ctas_1mo_pct_change)[0, 1]
spx_cei_cov = np.cov(cei_pct_change, spx_1mo_pct_change)[0, 1]
ctas_cei_cov = np.cov(cei_pct_change, ctas_1mo_pct_change)[0, 1]
ctas_earnings_cei_cov = np.cov(cei_ctas_pct_change, ctas_earnings_pct_change)[0, 1]
aapl_earnings_cei_cov = np.cov(cei_aapl_pct_change, aapl_earnings_pct_change)[0, 1]
pg_earnings_cei_cov = np.cov(cei_pg_pct_change, pg_earnings_pct_change)[0, 1]
dhi_earnings_cei_cov = np.cov(cei_dhi_pct_change, dhi_earnings_pct_change)[0, 1]
spx_earnings_cei_cov = np.cov(cei_pct_change, spx_earnings_pct_change)[0, 1]

print("CTAS/SPX Beta:", spx_ctas_cov / var_spx)
print("SPX/CEI Beta:", spx_cei_cov / var_cei)
print("CTAS/CEI Beta:", ctas_cei_cov / var_cei)
print("CTAS Earnings/CEI Beta:", ctas_earnings_cei_cov / var_cei_ctas)
print("AAPL Earnings/CEI Beta:", aapl_earnings_cei_cov / var_cei_aapl)
print("PG Earnings/CEI Beta:", pg_earnings_cei_cov / var_cei_pg)
print("DHI Earnings/CEI Beta:", dhi_earnings_cei_cov / var_cei_dhi)
print("SPX Earnings/CEI Beta:", spx_earnings_cei_cov / var_cei)