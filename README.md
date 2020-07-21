# Glyph - A highly customizable prompt

Example:

```shell
glyph
~/development/ : master - : myapp-jlmdf0py3.8
 %
```

Glyph is customized through `Item`. `Item` are small classes that are responsible for gathering and formatting
information.

Example:

```python
# plugins should be under the `glyph.items` namespace
# this project would have the following structure:
# glyph-weather/
# └── glyph
#   └── items
#       └── weather
#           ├── __init__.py
#           └── weather.py
from glyph.item import Item

class WeatherItem(Item):
    """Get the weather for a zip code."""
```
