from dataclasses import dataclass
from typing import Optional, TypedDict, NotRequired

from django_umami.utils import get_setting

import requests


@dataclass
class UmamiResponse:
    success: bool
    message: str


@dataclass
class UmamiConfig:
    host_url: str
    website_id: str

    def set_host_url(self, host_url: str):
        self.host_url = host_url

    def set_website_id(self, website_id: str):
        self.website_id = website_id


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

    def check_website_settings(self):
        if not self.options.host_url or not self.options.website_id:
            return UmamiResponse(False, "You must set the UMAMI_PAGE_URL and UMAMI_WEBSITE_ID variables in django settings.")
        return True

    def send(self, payload: UmamiPayload):
        if isinstance((valid_settings := self.check_website_settings()), UmamiResponse):
            return valid_settings

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
        elif isinstance(event, dict):
            return self.send(payload=UmamiPayload(website=website_id, data=event))
        else:
            return UmamiResponse(success=False, message="Invalid event data")


try:
    MAIN_PAGE_URL = get_setting("UMAMI_PAGE_URL", "")
    MAIN_WEBSITE_ID = get_setting("UMAMI_WEBSITE_ID", "")
except AttributeError:
    MAIN_PAGE_URL = None
    MAIN_WEBSITE_ID = None

umami = Umami(options=UmamiConfig(host_url=MAIN_PAGE_URL, website_id=MAIN_WEBSITE_ID))

"""
Usage:

import django_umami.core
import django_umami.decorators

django_umami.core.umami.options.set_host_url("https://example.com")
django_umami.core.umami.options.set_website_id("123456")


@django_umami.decorators.track("someone went to django view!")
def django_view(request):
    ...


def my_function():
    django_umami.core.umami.track("someone went to my function!")

    data = django_umami.core.UmamiEventData(
        hostname="example.com",
        language = "en-GB",
        referrer = "",
        screen = "1920x1080",
        title = "abc",
        url = "/my_event",
        name = "My Custom Event"
    )
    
    django_umami.core.umami.track(data)
    
    django_umami.core.umami.track({
        "name": "My Custom Event",
        "url": "/my_page/123"
    })
"""
