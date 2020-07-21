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

Customization of `glyph` is done using a `YAML` file, to pass arguments to constructors. Top-level options
in the configuration file are from `Prompt` and the `items` should be a mapping of `Item` to the desired arguments.

## Custom Items

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
