#!/usr/bin/env python3

# from pydantic_core.core_schema import ExpectedSerializationTypes
import requests
import os
from dotenv import load_dotenv
import json
from dataclasses import dataclass
# from pydantic import BaseModel, Field
# from typing import Optional

from dacite import from_dict, Config



# @dataclass
# class Current:
#     last_updated_epoch: int
#     last_updated: str
#     temp_c: float
#     temp_f: float
#     is_day: int
#     condition: Condition
#     wind_mph: float
#     wind_kph: float
#     wind_degree: int
#     wind_dir: str
#     pressure_mb: float
#     pressure_in: float
#     precip_mm: float
#     precip_in: float
#     humidity: int
#     cloud: int
#     feelslike_c: float
#     feelslike_f: float
#     windchill_c: float
#     windchill_f: float
#     heatindex_c: float
#     heatindex_f: float
#     dewpoint_c: float
#     dewpoint_f: float
#     vis_km: float
#     vis_miles: float
#     uv: float
#     gust_mph: float
#     gust_kph: float
#     short_rad: float
#     diff_rad: float
#     dni: float
#     gti: float


@dataclass
class Condition:
    text: str
    icon: str
    code: int

@dataclass
class AirQuality:
    co: float
    no2: float
    o3: float
    so2: float
    pm2_5: float
    pm10: float
    us_epa_index: int
    gb_defra_index: int    


@dataclass
class Current:
    last_updated_epoch: int
    last_updated: str
    temp_c: float
    temp_f: float
    is_day: int
    condition: Condition
    wind_mph: float
    wind_kph: float
    wind_degree: int
    wind_dir: str
    pressure_mb: float
    pressure_in: float
    precip_mm: float
    precip_in: float
    humidity: int
    cloud: int
    feelslike_c: float
    feelslike_f: float
    windchill_c: float
    windchill_f: float
    heatindex_c: float
    heatindex_f: float
    dewpoint_c: float
    dewpoint_f: float
    vis_km: float
    vis_miles: float
    uv: float
    gust_mph: float
    gust_kph: float
    air_quality: AirQuality
    short_rad: float
    diff_rad: float
    dni: float
    gti: float


@dataclass
class Location:
    name: str
    region: str
    country: str
    lat: float
    lon: float
    tz_id: str
    localtime_epoch: int
    localtime: str


@dataclass
class WeatherData:
    location: Location
    current: Current

def load_api_key(user_api_key: str) -> str | None:
    api_length: int = 21
    if user_api_key == "":
        load_dotenv()
        stored_api_Key = os.getenv("WEATHER_API_KEY")
        return stored_api_Key
    elif len(user_api_key) >= api_length:
        return user_api_key
    else:
        print("Invalid API")
        exit()

        
def get_query_from_user() -> str:
    input_str: str = input("Entry city name, IP address, Latitude/Longitude (decimal degree), US Zipcode, Uk Postcode, Canada Postalcode\n: ")
    if input_str == "":
        print("Please provide any of the following! \nCity name, IP address, Latitude/Longitude (decimal degree)\nUS Zipcode, Uk Postcode, Canada Postalcode: ")
        exit()
    return input_str




wind_arrows = {
    "N": "⬆",     # U+2B06
    "NNE": "↗",   # U+2197
    "NE": "↗",
    "ENE": "➡",   # U+27A1
    "E": "➡",
    "ESE": "↘",   # U+2198
    "SE": "↘",
    "SSE": "⬇",   # U+2B07
    "S": "⬇",
    "SSW": "↙",   # U+2199
    "SW": "↙",
    "WSW": "⬅",   # U+2B05
    "W": "⬅",
    "WNW": "↖",   # U+2196
    "NW": "↖",
    "NNW": "⬆",
}


US_EPA_INDEX = {
    1: "Good",
    2: "Moderate",
    3: "Unhealthy for sensitive group",
    4: "Unhealthy",
    5: "Very Unhealthy",
    6: "Hazardous"
}

GB_DEFRA_INDEX = {
    1: "Low",
    2: "Low",
    3: "Low",
    4: "Moderate",
    5: "Moderate",
    6: "Moderate",
    7: "High",
    8: "High",
    9: "High",
    10: "Very High"
}

def fetch_json():
    api_key : str | None = load_api_key("")

    # Exit, if no user and store api is found
    if api_key == None:
        print("API Not found")
        exit()

    query:str = get_query_from_user()
    # query: str = "London"
    aqi: str = "yes"
    url: str = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={query}&aqi={aqi}"
    # print(url)

    response = requests.get(url)

    if response.status_code != 200:
        print("Could not fetch weather data\nStatus Code: {}", response.status_code )

    json_body = response.json()

    return json_body 


def main():
    json_body = fetch_json()
    # print(json_body)
  
    try:
          # Map JSON keys to dataclass field names
        transform_keys = {
            "us-epa-index": "us_epa_index",
            "gb-defra-index": "gb_defra_index"
        }
        raw_aq = json_body["current"]["air_quality"]
        # Convert JSON keys to match dataclass field names

        normalized_data = {
            transform_keys.get(k, k): v for k, v in raw_aq.items()
        }
        json_body["current"]["air_quality"] = normalized_data
        air_quality = from_dict(data_class=AirQuality, data=normalized_data)
    except Exception as _:
        print("Failed to serialize air_quality fields")
    
    try:
        weather = from_dict(data_class=WeatherData, data=json_body)
    except Exception as _:
        print("Failed to fetch data, Invalid Location")
        exit()
    # conditon_icon = "🌥️"
    BOLD = "\033[1m"
    ITALIC = "\x1B[3m"
    RESET = "\033[0m"

    # print(weather)
    wind_dir = weather.current.wind_dir;
    wind_direction = wind_arrows[wind_dir]

    print("-" * 60)
    print(f"{BOLD}{weather.location.name}, {weather.location.region}, {weather.location.country}{RESET}")
    print()
    print(f"{BOLD}{weather.current.condition.text}{RESET}\t {weather.current.temp_c}°C | {weather.current.temp_f}°F")
    print(f"{ITALIC}Feels like{RESET} {weather.current.feelslike_c}°C | {weather.current.feelslike_f}°F")
    print()
    # print(weather.current.air_quality.us_epa_index)   # 2
    us_epa_index = weather.current.air_quality.us_epa_index;
    print(f"Humidity: {weather.current.humidity}%\t Cloud Cover: {weather.current.cloud}%")
    print(f"Dew Points: {weather.current.dewpoint_c}°C | {weather.current.dewpoint_f}°F   Wind: {weather.current.wind_kph}kph | {weather.current.wind_mph}mph {wind_direction}")
    print()
    print(f"Air Quality Index: {US_EPA_INDEX[us_epa_index]}\nPM10: {weather.current.air_quality.pm10} PM2.5: {weather.current.air_quality.pm2_5}")
    print("-" * 60)

    
    
        

    

    
    

    
        
if __name__ == "__main__":
    main()
