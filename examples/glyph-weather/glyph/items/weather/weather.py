"""Current weather status as an Item."""

from dataclasses import dataclass
import typing as T
import json
from enum import Enum

import requests
from logzero import logger

from glyph.item import Item

BASE_URL: str = "https://api.openweathermap.org/data/2.5/weather?"


class WeatherUnits(Enum):

    kelvin = 0
    metric = 1
    imperial = 2


@dataclass
class WeatherItem(Item):
    """Current weather status as an Item."""

    api_key: str
    city_name: str
    state_code: T.Optional[str] = None
    country_code: T.Optional[str] = None
    units: str = "imperial"
    temperature: bool = True
    condition: bool = True

    def __post_init__(self):
        # validate the enum
        self.units = WeatherUnits[self.units]

    def get(self) -> T.Dict:
        request_url = f"{BASE_URL}q={self.city_name}"
        if self.state_code is not None:
            assert self.country_code is not None
            request_url += f",{self.state_code},{self.country_code}"
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

    def __repr__(self) -> str:
        _resp = self.get()
        return " ".join(_resp.values())
