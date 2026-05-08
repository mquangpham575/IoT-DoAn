from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import sqlite3
import joblib
import os
from datetime import datetime
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Configuration
API_KEY = "IOT_SECRET_2026"
DB_PATH = "iot_data.db"
MODEL_PATH = "comfort_model.pkl"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temp REAL, humid REAL, light REAL, gas INTEGER, noise INTEGER,
            comfort_level INTEGER, timestamp DATETIME
        )
    ''')
    conn.commit()
    conn.close()

model = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None

class SensorPayload(BaseModel):
    temperature: float
    humidity: float
    light: float
    gas: int
    noise: int

@app.on_event("startup")
def startup():
    init_db()

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.post("/data")
async def receive_data(data: SensorPayload, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    comfort_level = int(model.predict([[data.temperature, data.humidity, data.gas]])[0]) if model else -1
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO sensor_readings (temp, humid, light, gas, noise, comfort_level, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (data.temperature, data.humidity, data.light, data.gas, data.noise, comfort_level, now))
    conn.commit()
    conn.close()
    
    return {"status": "success", "comfort": comfort_level}

@app.get("/history")
def get_history(limit: int = 20):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sensor_readings ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
