from typing import Any

from googleapiclient.discovery import (
    build,
)
import os
import re


class Video:
    def __init__(
        self,
        permalink: str,
        developerKey: str = None,
    ) -> None:
        if not developerKey:
            developerKey = os.getenv(
                "YOUTUBE_DATA_API_KEY",
                default="",
            )

            if developerKey == "":
                raise ValueError(
                    "'YOUTUBE_DATA_API_KEY' of enviroment variable is invalid",
                )

        # NOTE:
        # > Format for ID of YouTube video
        # https://webapps.stackexchange.com/a/54448
        matches = re.match(
            r"(^https:\/\/www\.youtube\.com\/watch\?v=|)(?P<id>[\-\w]{11})$",
            permalink,
        )

        if not matches:
            raise ValueError(
                "'%s' is incomplete ID" % permalink,
            )

        self.__id__ = matches.group("id")

        youtube = build(
            "youtube",
            "v3",
            developerKey=developerKey,
        )

        # NOTE:
        # https://developers.google.com/youtube/v3/docs/videos
        result = (
            youtube.videos()
            .list(
                id=self.__id__,
                part="contentDetails",
            )
            .execute()
        )

        items = result["items"]

        if len(items) != 1:
            raise Exception(
                "'%s' is unavailable" % self.__id__,
            )

        item = items[0]["contentDetails"]

        # NOTE:
        # > Durations define the amount of intervening time in a time interval
        # > and are represented by the format P[n]Y[n]M[n]DT[n]H[n]M[n]S or P[n]W as shown on the aside.
        # https://en.wikipedia.org/wiki/ISO_8601#Durations
        duration_iso8601 = item["duration"]

        matches = re.match(
            r"P(?:(\d+)D)?T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?",
            duration_iso8601,
        )

        if not matches:
            raise Exception(
                "'%s' is invalid ISO 8601 duration format" % duration_iso8601,
            )

        d = int(matches.group(1)) if matches.group(1) else 0
        h = int(matches.group(2)) if matches.group(2) else 0
        m = int(matches.group(3)) if matches.group(3) else 0
        s = int(matches.group(4)) if matches.group(4) else 0

        self.__duration__ = d * 86400 + h * 3600 + m * 60 + s

        # NOTE:
        # https://developers.google.com/youtube/v3/docs/videos?hl=ja#contentDetails.regionRestriction
        self.__region_restriction__ = item.get("regionRestriction")

        self.__allowed_regions__ = []
        self.__blocked_regions__ = []

        if self.__region_restriction__:
            allowed = self.__region_restriction__.get("allowed")
            blocked = self.__region_restriction__.get("blocked")

            if allowed:
                self.__allowed_regions__ = allowed

            if blocked:
                self.__blocked_regions__ = blocked

    @property
    def id(
        self,
    ) -> str:
        return self.__id__

    @property
    def duration(
        self,
    ) -> int:
        return self.__duration__

    @property
    def region_restriction(
        self,
    ) -> bool:
        return self.__region_restriction__ != None

    @property
    def allowed_regions(
        self,
    ) -> list[str]:
        return self.__allowed_regions__

    @property
    def blocked_regions(
        self,
    ) -> list[str]:
        return self.__blocked_regions__
