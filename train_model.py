# train_model.py
import pandas as pd
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression
import joblib

# 1. Hämta data från SQLite-databasen (Backend-kravet!)
engine = create_engine("sqlite:///games.db")
df = pd.read_sql("SELECT * FROM games", engine)

# 2. Rensa data för modellen (ta bort rader där betyg eller försäljning saknas)
model_df = df.dropna(subset=['critic_score', 'total_sales'])

# 3. Välj Features (X) och Target (y)
X = model_df[['critic_score']]  # Kan utökas med fler variabler
y = model_df['total_sales']

# 4. Träna modellen
model = LinearRegression()
model.fit(X, y)

# 5. Spara modellen till en fil så att Streamlit kan ladda den
joblib.dump(model, "sales_model.pkl")

print(f" AI-modellen tränad och sparad som 'sales_model.pkl'! Koefficient: {model.coef_[0]:.4f}")