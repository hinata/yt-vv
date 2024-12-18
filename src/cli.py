from typing import Any

import argparse
import json
import youtube

DEFAULT_MIN_DURATION = 15
DEFAULT_MAX_DURATION = 900
DEFAULT_REGIONS = [
    "JP",
]


def main() -> None:
    ap = argparse.ArgumentParser(
        description="the yt-vv is YouTube video validator",
    )

    ap.add_argument(
        "permalinks",
        type=str,
        nargs="*",
        help="YouTube video IDs to validate",
    )

    ap.add_argument(
        "--min-duration",
        type=int,
        default=DEFAULT_MIN_DURATION,
        help="allowed minimum duration of YouTube video (unit is seconds)",
    )

    ap.add_argument(
        "--max-duration",
        type=int,
        default=DEFAULT_MAX_DURATION,
        help="allowed maximum duration of YouTube video (unit is seconds)",
    )

    ap.add_argument(
        "--regions",
        type=str,
        nargs="*",
        default=DEFAULT_REGIONS,
        help="allowed regions of YouTube video (uint is ISO 3166-1 alpha-2)",
    )

    ap.add_argument(
        "--show-error",
        action="store_true",
        help="show error message with YouTube video ID",
    )

    args = ap.parse_args()

    for permalink in args.permalinks:
        try:
            v = youtube.Video(
                permalink=permalink,
            )
        except Exception as error:
            if args.show_error:
                print(
                    json.dumps(
                        dict(
                            id=permalink,
                            error=str(error),
                        ),
                    ),
                )

            continue

        if v.duration < args.min_duration:
            if args.show_error:
                print(
                    json.dumps(
                        dict(
                            id=v.id,
                            error="must be more than %d seconds" % args.min_duration,
                        ),
                    ),
                )

            continue

        if v.duration > args.max_duration:
            if args.show_error:
                print(
                    json.dumps(
                        dict(
                            id=v.id,
                            error="must be less than %d seconds" % args.max_duration,
                        ),
                    ),
                )

            continue

        has_region_error = False

        if len(v.allowed_regions) != 0:
            for r in args.regions:
                if not r in v.allowed_regions:
                    has_region_error = True

                    break

        if len(v.blocked_regions) != 0:
            for r in args.regions:
                if     r in v.blocked_regions:
                    has_region_error = True

                    break

        if has_region_error:
            if args.show_error:
                print(
                    json.dumps(
                        dict(
                            id=v.id,
                            error="this video is NOT allowed watch in '%s'" % r,
                        ),
                    ),
                )

            continue

        print(
            json.dumps(
                dict(
                    id=v.id,
                ),
            ),
        )
