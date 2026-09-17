import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

df = pd.read_csv("CSV Files/Video Games Data.csv")
st.write(df)
st.write("Video Game Dataset")

st.header("Top Selling Games")
top_games = df.sort_values("total_sales", ascending=False).head(10)
st.dataframe(top_games[["title", "console", "genre", "total_sales"]])