import requests
from datetime import datetime
from sqlalchemy.orm import Session
from backend.app.database import SessionLocal
from backend.app.models import Zone, Indicator

TARGET_ZONES = [
    {"name": "Paris", "postal_code": "75000", "lat": 48.8566, "lon": 2.3522},
    {"name": "Lyon", "postal_code": "69000", "lat": 45.7640, "lon": 4.8357},
    {"name": "Marseille", "postal_code": "13000", "lat": 43.2965, "lon": 5.3698}
]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def fetch_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("current_weather", {})
    except Exception:
        return None

def fetch_air_quality(lat, lon):
    url = f"https://api.openaq.org/v2/latest?coordinates={lat},{lon}&radius=10000&limit=1"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        if results:
            return results[0].get("measurements", [])
        return []
    except Exception:
        return []

def run_ingestion():
    db = next(get_db())
    print("Starting data ingestion...")

    for zone_data in TARGET_ZONES:
        zone = db.query(Zone).filter(Zone.name == zone_data["name"]).first()
        if not zone:
            zone = Zone(name=zone_data["name"], postal_code=zone_data["postal_code"])
            db.add(zone)
            db.commit()
            db.refresh(zone)
            print(f"Created zone: {zone.name}")
        else:
            print(f"Zone found: {zone.name}")

        weather_data = fetch_weather(zone_data["lat"], zone_data["lon"])
        if weather_data:
            temp_indicator = Indicator(
                type="temperature",
                source="Open-Meteo",
                value=weather_data.get("temperature"),
                unit="C",
                zone_id=zone.id,
                timestamp=datetime.now()
            )
            wind_indicator = Indicator(
                type="windspeed",
                source="Open-Meteo",
                value=weather_data.get("windspeed"),
                unit="km/h",
                zone_id=zone.id,
                timestamp=datetime.now()
            )
            db.add(temp_indicator)
            db.add(wind_indicator)
            print(f"  - Weather data added for {zone.name}")

        air_data = fetch_air_quality(zone_data["lat"], zone_data["lon"])
        for measurement in air_data:
            aq_indicator = Indicator(
                type=f"air_quality_{measurement['parameter']}",
                source="OpenAQ",
                value=measurement['value'],
                unit=measurement['unit'],
                zone_id=zone.id,
                timestamp=datetime.now()
            )
            db.add(aq_indicator)
            print(f"  - Air quality ({measurement['parameter']}) added for {zone.name}")

        db.commit()

    print("Ingestion complete.")

if __name__ == "__main__":
    run_ingestion()