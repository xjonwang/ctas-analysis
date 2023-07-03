from typing import *;
import os;
from dotenv import load_dotenv;
import pandas as pd;
import requests;

load_dotenv("./env/development.env")
alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

def getEarnings(
        symbol: str,
):
    earnings = pd.DataFrame(requests.get(f"https://www.alphavantage.co/query?function=INCOME_STATEMENT", params={ "symbol": symbol, "apikey": alpha_vantage_api_key }).json()["quarterlyReports"])[::-1]
    earnings.rename(columns={"fiscalDateEnding": "Date"}, inplace=True)
    earnings.to_csv("./data/AAPL-EARNINGS.csv", index=False)
    earnings.reset_index(drop=True, inplace=True)
    earnings_pct_change = list(earnings.operatingIncome.astype(float).pct_change()[1:])
    return {
        "earnings": earnings,
        "earnings_pct_change": earnings_pct_change
    }

def periodPctChange(
        df: pd.DataFrame,
        key: str,
        start_time: str,
        step: int,
        end_time: str = None
):
    df = df[df["Date"] >= start_time] if end_time == None else df[(df["Date"] >= start_time) & (df["Date"] <= end_time)]
    df.reset_index(drop=True, inplace=True)
    df = df[df.index % step == 0]
    return list(df[key].pct_change()[1:])
