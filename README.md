# EmiratesAIWeatherUpdate

A Python application that fetches and displays current weather conditions for cities across the UAE (United Arab Emirates) using the [OpenWeatherMap API](https://openweathermap.org/api).

## Features

- Retrieves real-time weather data for all seven UAE emirates
- Shows temperature, feels-like temperature, humidity, wind speed, and sky conditions
- Accepts custom city names as command-line arguments

## Requirements

- Python 3.8+
- A free [OpenWeatherMap API key](https://home.openweathermap.org/users/sign_up)

## Setup

1. Clone the repository and navigate into it:

   ```bash
   git clone https://github.com/M-quantum-tech/EmiratesAIWeatherUpdate.git
   cd EmiratesAIWeatherUpdate
   ```

2. Set your API key as an environment variable:

   ```bash
   export OPENWEATHER_API_KEY=your_api_key_here
   ```

## Usage

Run the application to get weather updates for all UAE cities:

```bash
python weather.py
```

Or specify one or more cities:

```bash
python weather.py Dubai "Abu Dhabi" Sharjah
```

### Sample output

```
=== Emirates AI Weather Update ===

  City       : Dubai, AE
  Condition  : Clear sky
  Temperature: 38.5°C (feels like 42.0°C)
  Humidity   : 55%
  Wind Speed : 3.2 m/s
```

## Running Tests

```bash
python -m unittest test_weather -v
```

## Cities Covered by Default

- Dubai
- Abu Dhabi
- Sharjah
- Ajman
- Ras al-Khaimah
- Fujairah
- Umm al-Quwain