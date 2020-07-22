<!--- vi: ft=markdown -->
# Glyph - A highly customizable prompt

**Glyph requires Python 3.8+**

To install `glyph`:

```shell
pip install git+https://github.com/sandal-tan/glyph

```

Glyph is a configurable prompt, driven by a YAML file to provide customization. By default, Glyph will display:

1. The current working directory
2. Git repository status
3. Python virtualenv name

```shell
 ~/development/glyph : master * : glyph-H1rWdwPe-py3.8
 %
```

Glyph also provides other `Item` to customize your prompt:

1. `ExitCodeItem` - Display the exit code of the previous command

## Why?

I couldn't find any off-the-shell fish prompts that I liked, and I really didn't like maintaining my own in fish/bash/
etc. so I wrote a framework to describe what I want simply, and make adding new items to my prompt fairly easy.

The default design is driven from my use-case at work. I copy and paste a lot from the terminal

The name: I have trouble coming up with names that aren't acronyms from a description. So I asked a friend. They
suggested systems responsible for dealing with fish. We stubmled upon "Great Lake Fish Fence" -> "glff" -> "glyph".

## Customization

In order to customize your prompt, create and edit `~/.glyph.yaml`:

```yaml
# ~/.glyph.yaml
info_location: 2 # inline
prompt_string: '>'
info_separator: '-'
items:
    ExitCodeItem: {}
    DirItem:
        expand_user: true
```

Which results in:

```shell
 127 - /U/i/d/glyph >
```

Customization of `glyph` is done using a `YAML` file, to pass arguments to constructors. Top-level options
in the configuration file are from `Prompt` and the `items` should be a mapping of `Item` to the desired arguments.

## Custom Items

Glyph is customized through `Item`. `Item` are small classes that are responsible for gathering and formatting
information.

Example:

```python
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

    @colorize(foreground_color=Foreground.MAGENTA)
    def __repr__(self) -> str:
        _resp = self.get()
        return " ".join(_resp.values())

```

When included an a prompt:

```shell
 ~/development/glyph : master * : 82º Clouds
 % 
```

# Integration

In order to get command status integration, the `$STATUS` variable must be set:

For Fish:

```
function export_status --on-event fish_postexec
    set -gx STATUS $status
end
```

# Cache

In order to speed up the prompt, the registry is saved to the local file system (by default at
`~/.cache/glyph/registry.pckl`) if the `Item`-set changes, this file should be manually deleted
