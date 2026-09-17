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

plt.figure(figsize=(10, 5))
plt.bar(top_games["title"], top_games["total_sales"])
plt.xticks(rotation=45, ha="right")
plt.xlabel("Game")
plt.ylabel("Total Sales")
plt.title("Top 10 Best Selling Games")

st.pyplot(plt)
