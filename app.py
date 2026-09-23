import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sqlalchemy import create_engine
import joblib

# --- 1. BACKEND: Hämta data från databasen ---
engine = create_engine("sqlite:///games.db")

@st.cache_data
def load_data():
    return pd.read_sql("SELECT * FROM games", engine)

df = load_data()

# --- 2. AI-MODELLERING: Ladda tränad modell och gör förutsägelse ---

st.header("AI Predictor: Förutsäg försäljning baserat på Critic Score")
try:
    model = joblib.load("sales_model.pkl")
    
    input_score = st.number_input("Ange förväntat Critic Score (0.0 - 10.0)", min_value=0.0, max_value=10.0, value=8.0, step=0.1)
    if st.button("Förutsäg försäljning"):
        predicted_sales = model.predict([[input_score]])[0]
        st.success(f"Förväntad totalförsäljning: **{max(0, predicted_sales):.2f} miljoner enheter**")
except Exception as e:
    st.warning("Hittade ingen sparad AI-modell. Kör `train_model.py` först för att generera den!")

st.markdown("---")

# --- 3. FRONTEND & VISUALISERING ---

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

st.header ("Search for a game")

search =st.text_input("Enter game title")

if search:
  result = df[df["title"].str.contains(search, case=False, na=False)]
  st.dataframe(result)
  
  st.header("Filter by Critic Score")
  
  score =st.slider("Minimum critic score", 0.0, 10.0, 7.0)

  filtered_games = df[df["critic_score"] >= score]
  
  st.dataframe(filtered_games)
  
  st.header("Sales by Genre")
  
  genre_sales = df.groupby("genre") ["total_sales"].sum()
  
  plt.figure(figsize=(10, 5))
  plt.bar(genre_sales.index, genre_sales.values)
  plt.xticks(rotation=45, ha="right")
  plt.xlabel("Genre")
  plt.ylabel("Total Sales")
  plt.title("Total Sales by Genre")
  
  st.pyplot(plt)
  
  st.header("Sales by Console")
  
  console_sales = df.groupby("console")["total_sales"].sum().sort_values(ascending=False).head(10)
  
  plt.figure(figsize=(10, 5))
  plt.bar(console_sales.index, console_sales.values)
  plt.xticks(rotation=45, ha="right")
  plt.xlabel("Console")
  plt.ylabel("Total Sales")
  plt.title("Total Sales by Console")
  
  st.pyplot(plt)
  
  st.header("Sales by Region")
  region_sales = {
    "North America": df["na_sales"].sum(),
    "Japan": df["jp_sales"].sum(),
    "Europe": df["pal_sales"].sum(),
    "Other": df["other_sales"].sum()
  }

  plt.figure(figsize=(10, 5))
  plt.bar(region_sales.keys(), region_sales.values())
  plt.xlabel("Region")
  plt.ylabel("Total Sales")
  plt.title("Total Sales by Region")
  
  st.pyplot(plt)
  
  st.header("games by release year")
  df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
  
  release_year =df["release_date"].dt.year.value_counts().sort_index()
  
  plt.figure(figsize=(10, 5))
  plt.plot(release_year.index, release_year.values)
  plt.xlabel("release year")
  plt.ylabel("Number of games")
  plt.title("games released by year")
  
  st.pyplot(plt)