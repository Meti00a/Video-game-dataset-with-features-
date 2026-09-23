# Video Game Dataset App

Guide för att installera och starta projektet lokalt.


## Installation & Start

### 1. Klona repositoryt
```bash
git clone https://github.com/Meti00a/Video-game-dataset-with-features-.git
cd Video-game-dataset-with-features-
```

### 2. Skapa och aktivera virtuell miljö (`.venv`)

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

> **Obs!** Om du får ett fel angående *Execution Policy* i PowerShell på Windows, kör detta kommando en gång först:  
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

*(När miljön är aktiverad ska `(.venv)` synas längst till vänster i terminalen).*

### 3. Installera beroenden
```bash
pip install -r requirements.txt
```

### 4. Starta applikationen
```bash
streamlit run app.py
```

Appen öppnas automatiskt i din webbläsare på `http://localhost:8501`.