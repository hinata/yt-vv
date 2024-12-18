# yt-vv

The yt-vv is YouTube video data validator by using YouTube data API v3.
You can verify the available if the inputed YouTube video ID is valid.

# How to use

## Requirements

- API KEY of [YouTube Data API v3](https://developers.google.com/youtube/v3/getting-started)
- python >= 3.10

## Install

```console
$ git clone https://github.com/hinata/yt-vv
$ pip install .
```

## For example, Run

```console
$ export YOUTUBE_DATA_API_KEY=****

$ yt-vv https://youtube.com/watch?v=MGt25mv4-2Q
{"id": "MGt25mv4-2Q"}

$ yt-vv --max-duration 30 https://youtube.com/watch?v=MGt25mv4-2Q

$ yt-vv --max-duration 30 --show-error https://youtube.com/watch?v=MGt25mv4-2Q
{"id": "MGt25mv4-2Q", error: "must be less than 30 seconds"}
```
