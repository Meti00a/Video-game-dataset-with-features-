# setup_db.py
import pandas as pd
from sqlalchemy import create_engine

# 1. Läs in CSV-filen
df = pd.read_csv("CSV Files/Video Games Data.csv")

# 2. Skapa SQLite-databas via SQLAlchemy
engine = create_engine("sqlite:///games.db")

# 3. Spara datan i en tabell som heter 'games'
df.to_sql("games", engine, if_exists="replace", index=False)

print("✅ Datan har sparas framgångsrikt i SQLite-databasen 'games.db'!")