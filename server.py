# FastAPI imports
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from collections import deque

# For I/O and Data handling
from fastapi.responses import StreamingResponse
import io
import csv

API_KEY = "key123"  # API key for authentication

# FastApi imports for authentication and verification
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key") # Request Header

# Dependency to verify API key
def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )

# Initialize FastAPI app
app = FastAPI(title="Telematics Data Receiver")

# Store the last 100 data points in memory (stores maximum 100 records)
data_log = deque(maxlen=100)

# expected data schema
# Pydantic model for incoming telematics data
class VehicleData(BaseModel):
    vehicle_id: str
    timestamp: str
    speed: float
    latitude: float
    longitude: float
    fuel_level: float
    engine_temp: float
    odometer: float

# POST endpoint to receive telematics data
@app.post("/telematics")
async def receive_telematics(
        data: VehicleData,
        api_key: str = Depends(verify_api_key)
):
    data_log.append(data.dict())
    return {"status": "success"}

# GET endpoint for an HTML dashboard showing recent data + a speed plot
@app.get("/", response_class=HTMLResponse)
async def show_latest_data():
    html = """
    <h2>Latest Vehicle Telematics Data</h2>
    <table border="1" cellpadding="5">
      <tr>
        <th>Vehicle ID</th>
        <th>Timestamp</th>
        <th>Speed (km/h)</th>
        <th>Latitude</th>
        <th>Longitude</th>
        <th>Fuel Level (%)</th>
        <th>Engine Temp (°C)</th>
        <th>Odometer (km)</th>
      </tr>
      {rows}
    </table>
    <br>
    <h2>Speed Over Time</h2>
    <img src="data:image/png;base64,{speed_plot}" alt="Speed Plot">
    """
    rows = ""
    for d in list(data_log)[-10:][::-1]: # Reverse to show latest first
        rows += f"<tr><td>{d['vehicle_id']}</td><td>{d['timestamp']}</td><td>{d['speed']}</td><td>{d['latitude']}</td><td>{d['longitude']}</td><td>{d['fuel_level']}</td><td>{d['engine_temp']}</td><td>{d['odometer']}</td></tr>"

    # Generate speed plot using matplotlib
    speeds = [d['speed'] for d in data_log]
    timestamps = [d['timestamp'] for d in data_log]

    import matplotlib.pyplot as plt
    import io
    import base64

    fig, ax = plt.subplots()
    ax.plot(timestamps, speeds, marker='o', linestyle='-')
    ax.set_title('Speed Over Time')
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Speed (km/h)')
    ax.tick_params(axis='x', rotation=45)
    fig.tight_layout()

    # Save plot to buffer and encode as base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    speed_plot = base64.b64encode(buf.getvalue()).decode('utf-8')

    # Inject rows and plot into the HTML template
    return html.format(rows=rows, speed_plot=speed_plot)


# API endpoint to get all data as JSON
@app.get("/data", response_model=List[VehicleData])
async def get_all_data(api_key: str = Depends(verify_api_key)):
    return list(data_log)



@app.get("/export_csv")
async def export_csv(api_key: str = Depends(verify_api_key)):
    # Create an in-memory CSV string
    output = io.StringIO()
    writer = csv.writer(output)
    # header row
    writer.writerow(["vehicle_id", "timestamp", "speed", "latitude", "longitude", "fuel_level", "engine_temp", "odometer"])
    # data rows
    for d in data_log:
        writer.writerow([d["vehicle_id"], d["timestamp"], d["speed"], d["latitude"], d["longitude"], d["fuel_level"], d["engine_temp"], d["odometer"]])
    output.seek(0)

    # Return as streaming response with CSV mime type
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=telematics_data.csv"}
    )

