"""
EmiratesAIWeatherUpdate
Fetches and displays current weather data for UAE cities.
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

UAE_CITIES = [
    "Dubai",
    "Abu Dhabi",
    "Sharjah",
    "Ajman",
    "Ras al-Khaimah",
    "Fujairah",
    "Umm al-Quwain",
]


def get_weather(city: str, api_key: str) -> dict:
    """Fetch current weather for a city using OpenWeatherMap API."""
    params = urllib.parse.urlencode({
        "q": f"{city},AE",
        "appid": api_key,
        "units": "metric",
    })
    url = f"{BASE_URL}?{params}"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"HTTP error fetching weather for {city}: {exc.code} {exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"URL error fetching weather for {city}: {exc.reason}") from exc


def format_weather(data: dict) -> str:
    """Format weather data into a human-readable string."""
    city = data.get("name", "Unknown")
    country = data.get("sys", {}).get("country", "")
    temp = data.get("main", {}).get("temp", "N/A")
    feels_like = data.get("main", {}).get("feels_like", "N/A")
    humidity = data.get("main", {}).get("humidity", "N/A")
    description = data.get("weather", [{}])[0].get("description", "N/A").capitalize()
    wind_speed = data.get("wind", {}).get("speed", "N/A")

    return (
        f"  City       : {city}, {country}\n"
        f"  Condition  : {description}\n"
        f"  Temperature: {temp}°C (feels like {feels_like}°C)\n"
        f"  Humidity   : {humidity}%\n"
        f"  Wind Speed : {wind_speed} m/s"
    )


def main(cities: list = None) -> None:
    """Fetch and print weather for one or more UAE cities."""
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    if not api_key:
        print("Error: OPENWEATHER_API_KEY environment variable is not set.", file=sys.stderr)
        print("Get a free API key at https://openweathermap.org/api", file=sys.stderr)
        sys.exit(1)

    if not cities:
        cities = UAE_CITIES

    print("=== Emirates AI Weather Update ===\n")
    for city in cities:
        try:
            data = get_weather(city, api_key)
            print(format_weather(data))
        except RuntimeError as exc:
            print(f"  [{city}] Error: {exc}", file=sys.stderr)
        print()


if __name__ == "__main__":
    requested = sys.argv[1:] if len(sys.argv) > 1 else None
    main(requested)
