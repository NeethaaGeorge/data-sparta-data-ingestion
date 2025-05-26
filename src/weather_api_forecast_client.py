import requests
import os
import configparser
import pandas as pd

def load_config():
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    config.read(config_path)
    return config['weatherapi']

def fetch_forecast_data():
    config = load_config()
    base_url = config['base_url']
    endpoint = config['forecast_endpoint']
    api_key = os.getenv("WEATHER_API_KEY")

    if not api_key:
        raise EnvironmentError("WEATHER_API_KEY environment variable not set.")

    url = f"{base_url}/{endpoint}"
    params = {
        "key": api_key,
        "q": "sydney",
        "days": 3,
        "aqi": "no",
        "alerts": "no"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch forecast: {e}")
        return None

def parse_forecast_data(data):
    location = data["location"]
    forecast_days = data["forecast"]["forecastday"]

    records = []

    for day in forecast_days:
        day_info = day["day"]
        condition = day_info["condition"]

        records.append({
            "date": day["date"],
            "location": location["name"],
            "region": location["region"],
            "country": location["country"],
            "max_temp_c": day_info["maxtemp_c"],
            "min_temp_c": day_info["mintemp_c"],
            "avg_temp_c": day_info["avgtemp_c"],
            "avg_humidity": day_info["avghumidity"],
            "condition": condition["text"],
            "precip_mm": day_info["totalprecip_mm"],
            "max_wind_kph": day_info["maxwind_kph"]
        })

    return records

def convert_to_csv(data, output_file):
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f" Forecast saved to: {output_file}")

if __name__ == "__main__":
    forecast_data = fetch_forecast_data()
    if forecast_data:
        parsed = parse_forecast_data(forecast_data)
        output_path = os.path.join(os.path.dirname(__file__), "weather_forecast.csv")
        convert_to_csv(parsed, output_path)