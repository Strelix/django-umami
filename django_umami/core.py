from dataclasses import dataclass, field
from typing import Optional, TypedDict, NotRequired, List

from django_umami.utils import get_setting

import requests

import logging

logger = logging.getLogger(__name__)


@dataclass
class UmamiResponse:
    success: bool
    message: str


@dataclass
class UmamiConfig:
    enabled: bool
    host_url: str
    website_id: str
    filter_page_paths: Optional[List[str]] = field(default_factory=list)
    filter_page_url_names: Optional[List[str]] = field(default_factory=list)
    session: Optional[requests.Session] = None
    filter_admin_pages: bool = False
    filter_superusers: bool = True
    filter_htmx: bool = False
    filter_anonymous: bool = False
    filter_media: bool = True
    filter_static: bool = True

    def create_session(self):
        self.session = requests.Session()

    def close_session(self):
        self.session.close()

    def set_enabled(self, enabled: bool):
        self.enabled = enabled

    def set_host_url(self, host_url: str):
        self.host_url = host_url

    def set_website_id(self, website_id: str):
        self.website_id = website_id

    def add_filter_page(self, page: str):
        self.filter_pages.append(page)


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
            data |= self.data
        return data


@dataclass
class Umami:
    options: UmamiConfig

    def check_website_settings(self):
        if not self.options.enabled:
            return UmamiResponse(False, "Tracking is disabled.")
        if not self.options.host_url or not self.options.website_id:
            logger.critical(
                "Failed to send event to umami. Please set both UMAMI_PAGE_URL and UMAMI_WEBSITE_ID vars."
            )
            return UmamiResponse(
                False, "You must set the UMAMI_PAGE_URL and UMAMI_WEBSITE_ID variables in django settings."
            )
        return True

    def send(self, payload: UmamiPayload):
        if isinstance((valid_settings := self.check_website_settings()), UmamiResponse):
            return valid_settings

        data = {"type": "event", "payload": payload.dict()}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        }

        if self.options.session:
            logger.info("Sending event to umami using session")
            return self.options.session.post(url=f"{self.options.host_url}/api/send", json=data, headers=headers)
        logger.info("Sending event to umami with no session")
        return requests.post(url=f"{self.options.host_url}/api/send", json=data, headers=headers)

    def track_event_name(self, event_name: str):
        payload = UmamiPayload(website=self.options.website_id, data={"name": event_name})
        return self.send(payload=payload)

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


MAIN_PAGE_URL = get_setting("UMAMI_PAGE_URL", "")
MAIN_WEBSITE_ID = get_setting("UMAMI_WEBSITE_ID", "")
ENABLED = get_setting("UMAMI_TRACKING_ENABLED", False)

if not MAIN_PAGE_URL or not MAIN_WEBSITE_ID:
    logger.warning(
        "Either one of UMAMI_PAGE_URL or UMAMI_WEBSITE_ID was not set in your environment variables. Make sure to set it manually!"
    )

if not ENABLED:
    logger.info("Django-Umami is disabled as the UMAMI_TRACKING_ENABLED environment variable is set to False.")

umami = Umami(options=UmamiConfig(enabled=ENABLED, host_url=MAIN_PAGE_URL, website_id=MAIN_WEBSITE_ID))

"""
Usage:

import django_umami.core
import django_umami.decorators

django_umami.core.umami.options.set_host_url("https://example.com")
django_umami.core.umami.options.set_website_id("123456")
django_umami.core.umami.options.create_session() # This allows requests to be bundled in one session allowing for up to ~3x faster requests

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
