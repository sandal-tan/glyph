# Glyph - A highly customizable prompt

Example:

```shell
glyph
~/development/myapp : master * : myapp-jlmdf0py3.8
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
