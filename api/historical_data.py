import requests
import csv
from tqdm import tqdm
import pandas as pd
import numpy as np
import yfinance as yf


def get_symbol(company):
    dic = {
    "tata" : "TATAMOTORS.NS",
    "tcs" : "TCS.NS",
    "infosys" : "INFY.NS",
    "hdfc" : "HDFCBANK.NS",
    "hdfc bank" : "HDFCBANK.NS",
    "hdfc bank limited" : "HDFCBANK.NS",
    "reliance" : "RELIANCE.NS",
    "adani ports" : "ADANIPORTS.NS",
    "asian paints" : "ASIANPAINT.NS",
    "axis bank" : "AXISBANK.NS",
    "bajaj auto" : "BAJAJ-AUTO.NS",
    "bajaj finance" : "BAJFINANCE.NS",
    "bajaj finserv" : "BAJAJFINSV.NS",
    "britannia" : "BRITANNIA.NS",
    "cipla" : "CIPLA.NS",
    "coal india" : "COALINDIA.NS",
    "divi's laboratories" : "DIVISLAB.NS",
    "dr. reddy's laboratories" : "DRREDDY.NS",
    "eicher motors" : "EICHERMOT.NS",
    "grasim industries" : "GRASIM.NS",
    "hcl technologies" : "HCLTECH.NS",
    "hdfc life insurance" : "HDFCLIFE.NS",
    "hero motocorp" : "HEROMOTOCO.NS",
    "hindalco industries" : "HINDALCO.NS",
    "hindustan unilever" : "HINDUNILVR.NS",
    "housing development finance" : "HDFC.NS",
    "icici bank" : "ICICIBANK.NS",
    "indusind bank" : "INDUSINDBK.NS",
    "infosys" : "INFY.NS",
    "itc" : "ITC.NS",
    "jsl" : "JSL.NS",
    "kotak mahindra bank" : "KOTAKBANK.NS",
    "larsen & toubro" : "LT.NS",
    "mahindra & mahindra" : "M&M.NS",
    "maruti suzuki" : "MARUTI.NS",
    "nestle india" : "NESTLEIND.NS",
    "ntpc" : "NTPC.NS",
    "oil & natural gas corporation" : "ONGC.NS",
    "power grid corporation" : "POWERGRID.NS",
    "reliance industries" : "RELIANCE.NS",
    "sbi" : "SBIN.NS",
    "shree cement" : "SHREECEM.NS",
    "sun pharmaceutical industries" : "SUNPHARMA.NS",
    "tata consumer products" : "TATACONSUM.NS",
    "tata steel" : "TATASTEEL.NS",
    "tech mahindra" : "TECHM.NS",
    "titan company" : "TITAN.NS",
    "ultratech cement" : "ULTRACEMCO.NS",
    "united spirits" : "MCDOWELL-N.NS",
    "wipro" : "WIPRO.NS"
}
    # return request_stock_price_list(dic[company.lower()], "full", "X8K4KA6JFZLEKH7V")
    print(dic[company.lower()])
    # return request_stock_price_list(dic[company.lower()], "compact", "2TFYCBX3QE03I549")
    return request_stock_price_list(dic[company.lower()], "1mo")
    

def request_stock_price_list(symbol, time):
    data = yf.download(f"{symbol}", period=f"{time}")
    return data


