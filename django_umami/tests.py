import unittest, requests
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase
from django_umami.core import Umami, UmamiConfig,UmamiResponse, UmamiEventData, UmamiPayload, umami
from django_umami.decorators import track, track_visit


class UmamiTests(TestCase):

    @classmethod
    def setUpClass(cls):
        # Mock settings attributes
        settings.UMAMI_PAGE_URL = "https://example.com"
        settings.UMAMI_WEBSITE_ID = "123456"
        settings.UMAMI_ENABLED = True

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.umami_config = UmamiConfig(
            host_url=settings.UMAMI_PAGE_URL, website_id=settings.UMAMI_WEBSITE_ID, enabled=settings.UMAMI_ENABLED
        )
        self.umami = Umami(options=self.umami_config)

    def test_umami_config(self):
        self.assertEqual(self.umami_config.host_url, "https://example.com")
        self.assertEqual(self.umami_config.website_id, "123456")

    def test_umami_send(self):
        with patch("requests.post") as mocked_post:
            mocked_post.return_value.status_code = 200

            payload = UmamiPayload(website="123456", data={"name": "test_event"})
            response = self.umami.send(payload)

            mocked_post.assert_called_once()
            self.assertEqual(response.status_code, 200)

    def test_umami_track_string_event(self):
        with patch.object(self.umami, "send") as mocked_send:
            mocked_send.return_value.status_code = 200

            self.umami.track("test_event")

            mocked_send.assert_called_once_with(payload=UmamiPayload(website="123456", data={"name": "test_event"}))

    def test_umami_track_dict_event(self):
        with patch.object(self.umami, "send") as mocked_send:
            mocked_send.return_value.status_code = 200

            event_data = UmamiEventData(name="test_event", url="/test-url")
            self.umami.track(event_data)

            mocked_send.assert_called_once_with(payload=UmamiPayload(website="123456", data=event_data))

    def test_umami_track_invalid_event(self):
        with patch.object(self.umami, "send") as mocked_send:
            mocked_send.return_value.status_code = 200

            res = self.umami.track(123)

            mocked_send.assert_not_called()

            # check if equals UmamiResponse(success=False, message="Invalid event data")
            self.assertEqual(res, UmamiResponse(False, "Invalid event data"))


if __name__ == "__main__":
    unittest.main()
