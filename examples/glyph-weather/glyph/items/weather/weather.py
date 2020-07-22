"""Current weather status as an Item."""

from dataclasses import dataclass
import typing as T
import json
from enum import Enum

import requests
from logzero import logger

from glyph.item import Item
from glyph.colors import colorize, Foreground

BASE_URL: str = "https://api.openweathermap.org/data/2.5/weather?"
"""The base URL used to build a request."""


class WeatherUnits(Enum):
    """The supported units of temperature."""

    kelvin = 0
    metric = 1
    imperial = 2


@dataclass
class WeatherItem(Item):
    """Current weather status as an Item.

    Args:
        api_key: Your OpenWeatherMap API key
        city_name: The name of the city for which current weather information is queried
        state_code: The code of the state in which ``city_name`` resides, ``country_code`` MUST be `us`
        country_code: The code of the country in which ``city_name, and optionally ``state_code`` exist
        units: The units of temperature to display
        temperature: Whether or not to display the temperature
        condition: Whether or not to display the current weather conditions

    """

    api_key: str
    city_name: str
    state_code: T.Optional[str] = None
    country_code: T.Optional[str] = None
    units: str = "imperial"
    temperature: bool = True
    condition: bool = True

    def __post_init__(self):
        # Validate the user input for units
        self.units = WeatherUnits[self.units]

    def get(self) -> T.Dict[str, str]:
        """Get the relevant data points from OpenWeatherMap.

        Returns:
            A dictionary containing the raw, relevant data points.

        """
        request_url = f"{BASE_URL}q={self.city_name}"
        if self.state_code is not None:
            assert self.country_code is not None
            request_url += f",{self.state_code}"
        if self.country_code is not None:
            request_url += f",{self.country_code}"
        request_url += f"&appid={self.api_key}&units={self.units.name}"

        logger.debug(request_url)
        response = requests.get(request_url)
        json_response = response.json()

        result = {}

        if json_response["cod"] != "404":
            if self.temperature:
                result["temperature"] = str(round(json_response["main"]["temp"])) + "º"
            if self.condition:
                result["condition"] = json_response["weather"][0]["main"]

        return result

    @colorize(foreground_color=Foreground.MAGENTA)
    def __repr__(self) -> str:
        _resp = self.get()
        return " ".join(_resp.values())
