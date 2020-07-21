# glyph-weather

Using [OpenWeatherMap][1], get the current weather conditions given a city, and optionally state and/or country code.

To install:

```shell
pip install .
```

In order to add `glyph-weather` as an `Item`, add the following to your `~/.glyph.yaml` after installing:

```yaml
# other Prompt config here
items:
    # other Item
    WeatherItem:
        api_key: '<your_api_key>'
        city_name: 'cambridge'
        state_code: 'ma'
        country_code: 'us'
    # other Item
```

[1]: https://openweathermap.org/current
