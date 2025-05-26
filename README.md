# Telematics Simulator

This project simulates a vehicle sending telematics data (like speed, location, and fuel level) to a backend server. The server is built with FastAPI and displays incoming data in real time, generates live charts, and lets you securely export everything as a CSV file.

---

## Features

- Simulates realistic vehicle data in Python
- FastAPI backend with automatic data validation
- Live dashboard with a data table and speed-over-time chart
- API key authentication for all data endpoints
- Download all data as CSV for analysis

---

## Tech Stack

- Python 3
- FastAPI & Uvicorn
- Requests
- Matplotlib

---

## How to Run

1. **Clone the repository and set up a virtual environment:**
    ```
    git clone https://github.com/Architrawat25/telematics-simulator.git
    cd telematics-simulator
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2. **Start the FastAPI server:**
    ```
    uvicorn server:app --reload
    ```

3. **Run the simulator in a separate terminal:**
    ```
    python simulator.py
    ```

---

## Dashboard

- Open [http://localhost:8000/](http://localhost:8000/) in your browser.
- You’ll see the latest vehicle data and a live chart of speed over time.

---

## Authentication

All data endpoints require an API key.

- Header: `X-API-Key`
- Default value: `key123` (see `server.py`)

Example using `curl` to download CSV:

## curl -H "X-API-Key: key123" http://localhost:8000/export_csv -o telematics_data.csv

---

## Example Screenshot

![Dashboard Screenshot](dashboard_screenshot.png)

---

## Possible Improvements

- Store data in a real database (SQL/NoSQL)
- Deploy to AWS or another cloud platform
- Add more charts or support for more vehicle sensors
- Use OAuth2/JWT for authentication

---

## Author

[Archit Rawat](https://github.com/Architrawat25)

---


