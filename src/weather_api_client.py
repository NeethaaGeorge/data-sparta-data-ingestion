import requests
import pandas as pd
import configparser
import os
import time
from urllib.parse import urljoin

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    config = configparser.ConfigParser()
    files = config.read(config_path)
    # print(f"files: {files} Loaded sections: {config.sections()}")  # Debug line
    return config['weatherapi']

def get_api_key():
    api_key = os.getenv('WEATHER_API_KEY')
    if not api_key:
        raise EnvironmentError("WEATHER_API_KEY environment variable not set.")
    return api_key

def fetch_weather_data(location: str = "sydney", aqi: str = "no", retries: int = 3, delay: int = 2):
    config = load_config()
    base_url = config['base_url']
    endpoint = config['endpoint']
    url = urljoin(f"{base_url}/", endpoint)
    api_key = get_api_key()

    params = {
        "key": api_key,
        "q": location,
        "aqi": aqi
    }

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            print("Response received successfully:")
            print(response.json())
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt < retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("All retry attempts failed.")
                raise

def parse_weather_json(data: dict) -> dict:
    """Extract and flatten all relevant fields from weather API JSON response."""
    location = data["location"]
    current = data["current"]
    condition = current["condition"]

    return {
        # Location fields
        "location_name": location["name"],
        "location_region": location["region"],
        "location_country": location["country"],
        "location_lat": location["lat"],
        "location_lon": location["lon"],
        "location_tz_id": location["tz_id"],
        "location_localtime_epoch": location["localtime_epoch"],
        "location_localtime": location["localtime"],

        # Current weather fields
        "current_last_updated_epoch": current["last_updated_epoch"],
        "current_last_updated": current["last_updated"],
        "current_temp_c": current["temp_c"],
        "current_temp_f": current["temp_f"],
        "current_is_day": current["is_day"],
        "current_condition_text": condition["text"],
        "current_condition_icon": condition["icon"],
        "current_condition_code": condition["code"],
        "current_wind_mph": current["wind_mph"],
        "current_wind_kph": current["wind_kph"],
        "current_wind_degree": current["wind_degree"],
        "current_wind_dir": current["wind_dir"],
        "current_pressure_mb": current["pressure_mb"],
        "current_pressure_in": current["pressure_in"],
        "current_precip_mm": current["precip_mm"],
        "current_precip_in": current["precip_in"],
        "current_humidity": current["humidity"],
        "current_cloud": current["cloud"],
        "current_feelslike_c": current["feelslike_c"],
        "current_feelslike_f": current["feelslike_f"],
        "current_windchill_c": current["windchill_c"],
        "current_windchill_f": current["windchill_f"],
        "current_heatindex_c": current["heatindex_c"],
        "current_heatindex_f": current["heatindex_f"],
        "current_dewpoint_c": current["dewpoint_c"],
        "current_dewpoint_f": current["dewpoint_f"],
        "current_vis_km": current["vis_km"],
        "current_vis_miles": current["vis_miles"],
        "current_uv": current["uv"],
        "current_gust_mph": current["gust_mph"],
        "current_gust_kph": current["gust_kph"]
    }

def convert_to_csv(data_dict: dict, output_path: str):
    """Convert the dict to DataFrame and save as CSV file."""
    df = pd.DataFrame([data_dict])
    df.to_csv(output_path, index=False)
    print(f"CSV saved to: {output_path}")

if __name__ == "__main__":
    raw_data = fetch_weather_data()
    if raw_data:
        parsed_data = parse_weather_json(raw_data)
        output_file = os.path.join(os.path.dirname(__file__), 'weather_data_full.csv')
        convert_to_csv(parsed_data, output_file)