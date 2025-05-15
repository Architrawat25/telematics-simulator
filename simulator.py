import requests # For sending HTTP requests to the server
import random
import time     # For timestamps and sleep intervals
import json     # For formatting data as JSON

# Configuration
SERVER_URL = "http://localhost:8000/telematics"  # FastAPI default port is 8000
TRANSMISSION_INTERVAL = 2  # 2 seconds time between transmission

def generate_vehicle_data(vehicle_id="CAR-001"):
    """Generate realistic simulated telematics data."""
    return {
        "vehicle_id": vehicle_id,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "speed": round(random.uniform(0, 120), 1),  # speed in km/h
        "latitude": round(random.uniform(28.60, 28.70), 6),  # Latitude: Delhi
        "longitude": round(random.uniform(77.10, 77.20), 6), # Longitude: Delhi
        "fuel_level": round(random.uniform(10, 100), 1),  # fuel in Percentage
        "engine_temp": round(random.uniform(80, 110), 1),  # Engine temperature in Celsius
        "odometer": round(random.uniform(5000, 150000), 1)  # reading in Kilometers
    }

def send_data(data):
    """Send data to FastAPI server with API key."""
    try:
        headers = {
            "Content-Type": "application/json", # JSON payload
            "X-API-Key": "key123"  # API_KEY in server.py
        }
        response = requests.post(SERVER_URL, data=json.dumps(data), headers=headers)
        print(f"Data sent: {data['timestamp']} | Status: {response.status_code}")
    except Exception as e:
        print(f"Transmission error: {str(e)}") # any network or serialization errors


if __name__ == "__main__":
    print("Starting telematics simulator...")
    while True:
        vehicle_data = generate_vehicle_data() # Create a new sample
        send_data(vehicle_data)                # Send to the server
        time.sleep(TRANSMISSION_INTERVAL)      # Wait before sending the next data point
