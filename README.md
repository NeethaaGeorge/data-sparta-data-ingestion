# Weather Data Ingestion - Last 6 Days (File Name - weather_api_history.py)

This script retrieves **hourly historical weather data** for the **last 6 days** from the [WeatherAPI](https://www.weatherapi.com/) for selected Australian cities and stores the results in a single CSV file.

## Features

- Fetches data for:
  - Sydney
  - Brisbane
  - Melbourne
  - Perth
- Extracts detailed **hourly weather metrics** (temperature, wind, humidity, UV, etc.)
- Combines results into one CSV file: 'weather_hourly_AUS_last_6_days.csv'
- Handles API access via secure configuration and environment variable
- Easily extendable for more dates or cities

## Project Structure
src/
├── config.ini
├── weather_api_history.py
├── weather_hourly_AUS_last_6_days.csv ← generated output

**1. Clone the repository**
`bash
git clone https://github.com/NeethaaGeorge/data-sparta-data-ingestion.git
cd data-sparta-data-ingestion/src

**2. Install dependencies**
pip install requests pandas

**3. Create your config.ini**

# config.ini
[weatherapi]
base_url = http://api.weatherapi.com/v1
endpoint = current.json
history_endpoint = history.json
forecast_endpoint = forecast.json
locations = Sydney,Brisbane,Melbourne,Perth

**4. Set your API key as an environment variable**

**5. Run the script**
python  weather_api_history.py

**6. Output**

File: weather_hourly_AUS_last_6_days.csv
