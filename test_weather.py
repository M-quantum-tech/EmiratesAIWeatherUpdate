"""Tests for EmiratesAIWeatherUpdate weather module."""

import json
import sys
import unittest
from io import StringIO
from unittest.mock import MagicMock, patch

import weather


SAMPLE_RESPONSE = {
    "name": "Dubai",
    "sys": {"country": "AE"},
    "main": {"temp": 38.5, "feels_like": 42.0, "humidity": 55},
    "weather": [{"description": "clear sky"}],
    "wind": {"speed": 3.2},
}


class TestFormatWeather(unittest.TestCase):
    def test_format_contains_city(self):
        result = weather.format_weather(SAMPLE_RESPONSE)
        self.assertIn("Dubai", result)

    def test_format_contains_temperature(self):
        result = weather.format_weather(SAMPLE_RESPONSE)
        self.assertIn("38.5", result)

    def test_format_contains_description(self):
        result = weather.format_weather(SAMPLE_RESPONSE)
        self.assertIn("Clear sky", result)

    def test_format_contains_humidity(self):
        result = weather.format_weather(SAMPLE_RESPONSE)
        self.assertIn("55%", result)

    def test_format_contains_wind(self):
        result = weather.format_weather(SAMPLE_RESPONSE)
        self.assertIn("3.2 m/s", result)

    def test_format_empty_data(self):
        result = weather.format_weather({})
        self.assertIn("Unknown", result)


class TestGetWeather(unittest.TestCase):
    def _make_mock_response(self, data):
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps(data).encode()
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        return mock_resp

    @patch("urllib.request.urlopen")
    def test_get_weather_success(self, mock_urlopen):
        mock_urlopen.return_value = self._make_mock_response(SAMPLE_RESPONSE)
        result = weather.get_weather("Dubai", "fake_key")
        self.assertEqual(result["name"], "Dubai")

    @patch("urllib.request.urlopen")
    def test_get_weather_http_error(self, mock_urlopen):
        import urllib.error
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="", code=401, msg="Unauthorized", hdrs=None, fp=None
        )
        with self.assertRaises(RuntimeError):
            weather.get_weather("Dubai", "bad_key")


class TestMain(unittest.TestCase):
    @patch.dict("os.environ", {}, clear=True)
    def test_main_no_api_key(self):
        os.environ.pop("OPENWEATHER_API_KEY", None)
        with self.assertRaises(SystemExit):
            weather.main()

    @patch("weather.get_weather", return_value=SAMPLE_RESPONSE)
    @patch.dict("os.environ", {"OPENWEATHER_API_KEY": "test"})
    def test_main_prints_output(self, mock_get):
        captured = StringIO()
        with patch("sys.stdout", captured):
            weather.main(["Dubai"])
        output = captured.getvalue()
        self.assertIn("Emirates AI Weather Update", output)


import os  # noqa: E402 (needed after class definitions above)

if __name__ == "__main__":
    unittest.main()
