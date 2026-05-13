# [DEPRECATED] This file is an old version. Use 'run.py' or 'app/main.py' for the modular backend.
from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
import uvicorn
import sqlite3
import joblib
import os
from datetime import datetime
import pandas as pd
from pydantic import BaseModel
from zeroconf.asyncio import AsyncZeroconf
from zeroconf import ServiceInfo
import socket
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
API_KEY = "IOT_SECRET_2026"
DB_PATH = os.path.join(BASE_DIR, "iot_data.db")
MODEL_PATH = os.path.join(BASE_DIR, "comfort_model.pkl")

def get_local_ip():
    """INTENT: Detect the local network IP address for mDNS advertisement."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.254.254.254', 1))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()

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

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database
    init_db()
    
    # Startup: mDNS Advertisement for Android App discovery
    local_ip = get_local_ip()
    zc = AsyncZeroconf()
    info = ServiceInfo(
        "_http._tcp.local.",
        "iot-health-monitor._http._tcp.local.",
        addresses=[socket.inet_aton(local_ip)],
        port=8000,
        properties={},
        server="iot-server.local.",
    )
    await zc.async_register_service(info)
    
    yield
    
    # Shutdown: Clean up mDNS
    await zc.async_unregister_service(info)
    await zc.async_close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

model = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None

class SensorPayload(BaseModel):
    temperature: float
    humidity: float
    light: float
    gas: int
    noise: int

def get_rule_base_comfort(t, h, g, l, n):
    """
    INTENT: Provide a deterministic safety fallback if AI fails or thresholds are critical.
    0: Nominal, 1: Warning, 2: Critical
    """
    if g > 3000 or t > 40: return 2 # Critical Danger
    if g > 2000 or t > 35 or h > 85 or l < 10 or n > 3000: return 1 # Warning
    return 0 # Normal

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.post("/data")
async def receive_data(data: SensorPayload, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    # 1. Rule-base assessment (Updated with Light & Noise sensitivity)
    rule_comfort = get_rule_base_comfort(data.temperature, data.humidity, data.gas, data.light, data.noise)

    # 2. AI Assessment (Nuanced comfort)
    ai_comfort = -1
    if model:
        # Note: Model currently trained on T, H, G only
        input_df = pd.DataFrame([[data.temperature, data.humidity, data.gas]], 
                                columns=['temp', 'humid', 'gas'])
        ai_comfort = int(model.predict(input_df)[0])

    # 3. Decision Logic: Maximize sensitivity across Hybrid Engine
    final_comfort = max(rule_comfort, ai_comfort)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO sensor_readings (temp, humid, light, gas, noise, comfort_level, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (data.temperature, data.humidity, data.light, data.gas, data.noise, final_comfort, now))
    conn.commit()
    conn.close()
    
    return {"status": "success", "comfort": final_comfort, "method": "hybrid"}

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
