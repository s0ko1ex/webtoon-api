# Webtoon python API

A python library for communicating with non-public Webtoon API.

## Usage example

```python
from webtoon_api import WebtoonApi

api = WebtoonApi()

episode = api.episodeInfo(
    titleNo=2702,
    episodeNo=1,
    serviceZone="GLOBAL",
    language="en",
    platform="APP_ANDROID"
)

with open("image.jpg", "wb") as file:
    file.write(
        api.get_static_content(episode["episodeInfo"]["imageInfo"][0]["url"])
    )
```

The general API call looks like

```python
api.<methodName>(<args>)
```

# Installation

Using pip

```shell
pip install webtoon-api
```

Using poetry directly from repository

```shell
pip install poetry
poetry install
```

# API reference

See [API.md](docs/API.md) in docs.

# How we got here

If you are interested in how this library was created, have a look at [Reverse-engineering.md](docs/Reverse-engineering.md) in docs