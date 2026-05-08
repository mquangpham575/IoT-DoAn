from fastapi import FastAPI, Request
import uvicorn
from datetime import datetime

app = FastAPI()

# Lưu trữ dữ liệu tạm thời (In-memory)
data_history = []

@app.post("/data")
async def receive_data(request: Request):
    json_data = await request.json()
    json_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Logic xử lý tại Edge (Member 4)
    status = "Normal"
    if json_data.get("temperature", 0) > 35:
        status = "ALERT: High Temperature!"
    elif json_data.get("gas", 0) > 2500:
        status = "ALERT: Gas Leakage Detected!"
        
    json_data["status"] = status
    data_history.append(json_data)
    
    print(f"[{json_data['timestamp']}] Received: {json_data}")
    return {"message": "Data received", "edge_status": status}

@app.get("/")
def read_root():
    return {"project": "IoT Environmental Monitoring", "history_count": len(data_history)}

if __name__ == "__main__":
    print("Starting Central Server at http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
