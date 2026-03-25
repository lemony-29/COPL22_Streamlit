import streamlit as st
import requests
from requests.exceptions import HTTPError
import pandas as pd

# Used to simplify getting the url for coingecko urls

def get_weburl(sub):
    return f"https://api.coingecko.com/api/v3/{sub}"

@st.cache_data
def fetch_data(api_url):
    response = requests.get(api_url)
    return response.json(), response

# Returns the id associated with the coin symbol

def fetch_coin_id_from_symbol(sym):
    nid = None
    try:
        data, response = fetch_data(get_weburl("coins/list"))
        response.raise_for_status()
    except HTTPError as e:
        st.error("Failed to fetch coin list: " + e.response.text)
    else:
        for d in data:
            if d["symbol"] == str.lower(sym):
                nid = d["id"]
                break
    finally:
        return nid
    
# ==================
# The chart at the top of the app

st.header("Top 10 markets on CoinGecko")

try:
    url = get_weburl("coins/markets")
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 10}
    data, response = fetch_data(url + "?" + "&".join(f"{k}={v}" for k, v in params.items()))
    response.raise_for_status()
except HTTPError as e:
    st.error("Failed to fetch coin market list: " + e.response.text)
else:
    df = pd.DataFrame(data)
    st.dataframe(df)

# ==================
# Inputbox to preview price data for a specific coin

specific_coin = st.text_input("Look for the price history of a specific coin? (enter symbol i.e \"btc\")")

if specific_coin != "":
    try:
        coins_list, response = fetch_data(get_weburl("coins/list"))
        response.raise_for_status()
    except HTTPError as e:
        st.error("Failed to fetch data for coin: " + e.response.text)
    else:
        st.text("Viewing data for " + specific_coin)

        id = fetch_coin_id_from_symbol(specific_coin)
        if id == None:
            st.error("Coin " + specific_coin + " could not be found.")
        else:
            try:
                info = fetch_data(get_weburl(f"coins/{id}"))
            except:
                st.error("Coin " + specific_coin + " could not be found.")
            else:
            #st.text(info[0])
                market_data = info[0]["market_data"]
            
                mk_d = [
                    ("Current Price", market_data["current_price"][specific_coin]),
                    ("Price Change in past year", market_data["price_change_percentage_1y_in_currency"][specific_coin]),
                    ("High 24h", market_data["high_24h"][specific_coin]),
                    ("Low 24h", market_data["low_24h"][specific_coin]),
                    ("Total Supply", market_data["total_supply"]),
                    ("Circulating Supply", market_data["circulating_supply"])
                ]

                i = 0
                for c in st.columns(len(mk_d)):
                    c.metric(mk_d[i][0], mk_d[i][1])
                    i += 1

