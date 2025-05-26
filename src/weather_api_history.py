import requests
import os
import configparser
import pandas as pd
from datetime import datetime, timedelta

def load_config():
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    config.read(config_path)
    return config['weatherapi']

def fetch_historical_weather(location, date_str):
    config = load_config()
    base_url = config['base_url']
    endpoint = config['history_endpoint']
    api_key = os.getenv("WEATHER_API_KEY")

    if not api_key:
        raise EnvironmentError("WEATHER_API_KEY environment variable not set.")

    url = f"{base_url}/{endpoint}"
    params = {
        "key": api_key,
        "q": location,
        "dt": date_str
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {location} on {date_str}: {e}")
        return None

def parse_hourly_weather(data):
    location = data["location"]
    forecast = data["forecast"]["forecastday"][0]

    hourly_records = []

    for hour in forecast["hour"]:
        record = {
            "date": forecast["date"],
            "time": hour["time"],
            "location": location["name"],
            "region": location["region"],
            "country": location["country"],
            "lat": location["lat"],
            "lon": location["lon"],
            "tz_id": location["tz_id"],
            "temp_c": hour["temp_c"],
            "temp_f": hour["temp_f"],
            "is_day": hour["is_day"],
            "condition_text": hour["condition"]["text"],
            "condition_icon": hour["condition"]["icon"],
            "wind_mph": hour["wind_mph"],
            "wind_kph": hour["wind_kph"],
            "wind_degree": hour["wind_degree"],
            "wind_dir": hour["wind_dir"],
            "pressure_mb": hour["pressure_mb"],
            "pressure_in": hour["pressure_in"],
            "precip_mm": hour["precip_mm"],
            "precip_in": hour["precip_in"],
            "humidity": hour["humidity"],
            "cloud": hour["cloud"],
            "feelslike_c": hour["feelslike_c"],
            "feelslike_f": hour["feelslike_f"],
            "windchill_c": hour.get("windchill_c"),
            "windchill_f": hour.get("windchill_f"),
            "heatindex_c": hour.get("heatindex_c"),
            "heatindex_f": hour.get("heatindex_f"),
            "dewpoint_c": hour.get("dewpoint_c"),
            "dewpoint_f": hour.get("dewpoint_f"),
            "will_it_rain": hour.get("will_it_rain"),
            "chance_of_rain": hour.get("chance_of_rain"),
            "will_it_snow": hour.get("will_it_snow"),
            "chance_of_snow": hour.get("chance_of_snow"),
            "vis_km": hour["vis_km"],
            "vis_miles": hour["vis_miles"],
            "gust_mph": hour["gust_mph"],
            "gust_kph": hour["gust_kph"],
            "uv": hour["uv"]
        }
        hourly_records.append(record)

    return hourly_records

def save_to_csv(data_list, output_path):
    df = pd.DataFrame(data_list)
    df.to_csv(output_path, index=False)
    print(f"Saved {len(data_list)} hourly records to {output_path}")

if __name__ == "__main__":
    config = load_config()
    locations = [loc.strip() for loc in config['locations'].split(',')]

    today = datetime.today()
    date_list = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(1, 7)]

    all_hourly_data = []

    for date_str in date_list:
        for loc in locations:
            print(f"Fetching weather for {loc} on {date_str}")
            raw_data = fetch_historical_weather(loc, date_str)
            if raw_data:
                parsed_records = parse_hourly_weather(raw_data)
                all_hourly_data.extend(parsed_records)

    if all_hourly_data:
        output_file = os.path.join(os.path.dirname(__file__), f"weather_hourly_AUS_last_6_days.csv")
        save_to_csv(all_hourly_data, output_file)
    else:
        print("No data was retrieved.")
