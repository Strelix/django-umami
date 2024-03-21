import json
import sys
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Literal, TypedDict, NotRequired

import requests

from django.conf import settings

MAIN_PAGE_URL = getattr(settings, "UMAMI_PAGE_URL")
MAIN_WEBSITE_ID = getattr(settings, "UMAMI_WEBSITE_ID")


@dataclass
class UmamiResponse:
    success: bool
    message: str


@dataclass
class UmamiConfig:
    host_url: str
    website_id: str


class UmamiEventData(TypedDict):
    hostname: NotRequired[str]
    language: NotRequired[str]
    referrer: NotRequired[str]
    screen: NotRequired[str]
    title: NotRequired[str]
    url: NotRequired[str]
    name: NotRequired[str]


@dataclass
class UmamiPayload:
    website: str
    data: Optional[UmamiEventData] = None

    def dict(self):
        data = {"website": self.website}
        if self.data:
            print("has data")
            data |= self.data
        return data


@dataclass
class Umami:
    options: UmamiConfig

    def send(self, payload: UmamiPayload):
        data = {"type": "event", "payload": payload.dict()}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        }
        print(f"Tracking data: \n {data}")
        return requests.post(url=f"{self.options.host_url}/api/send", json=data, headers=headers)

    def track(self, event: UmamiEventData | str, event_data=None):
        website_id = self.options.website_id

        if isinstance(event, str):
            payload = UmamiPayload(website=website_id, data={"name": str(event)})
            if event_data:
                payload.data = event_data

            return self.send(payload=payload)

        return self.send(payload=UmamiPayload(website=website_id, data=event))


umami = Umami(options=UmamiConfig(host_url=MAIN_PAGE_URL, website_id=MAIN_WEBSITE_ID))

"""
Usage:

from django_umami import main

data = main.UmamiEventData(
    hostname
    language="en-GB" # optional
    referrer="" # optional
    screen="1920x1080" # optional
    title="abc" # optional
    url="/myevent" # optional
    name="My Custom Event" # optional
)

main.umami.track(data)

# or you can just send with an event name

main.umami.track("My Custom Event")
"""
