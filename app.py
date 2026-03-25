import streamlit as st
import requests
import pandas as pd

@st.cache_data
def fetch_data(api_url):
    response = requests.get(api_url)
    return response.json()

option = st.selectbox("Select an option", ("test option", "second test option"))

print("selected option ", option)

# # Example: fetch top 10 coins from CoinGecko
# url = "https://api.coingecko.com/api/v3/coins/markets"
# params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 10}
# data = fetch_data(url + "?" + "&".join(f"{k}={v}" for k, v in params.items()))
# df = pd.DataFrame(data)

# # Assuming df has 'timestamp' and 'price' columns
# df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
# df = df.set_index('timestamp')
# st.line_chart(df['price'])
