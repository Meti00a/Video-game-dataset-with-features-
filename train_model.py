import pandas as pd
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression
import joblib

#  Hämta data från SQLite-databasen
engine = create_engine("sqlite:///games.db")
df = pd.read_sql("SELECT * FROM games", engine)

#  Rensa data för modellen
model_df = df.dropna(subset=['critic_score', 'total_sales'])

X = model_df[['critic_score']]  # Kan utökas med fler variabler
y = model_df['total_sales']

# Träna modellen
model = LinearRegression()
model.fit(X, y)

# Spara modellen till en fil så att Streamlit kan ladda den
joblib.dump(model, "sales_model.pkl")

print(f" AI-modellen tränad och sparad som 'sales_model.pkl'! Koefficient: {model.coef_[0]:.4f}")