from functools import wraps
from typing import Optional

from django.http import HttpRequest

from django_umami.core import umami, UmamiEventData


def track(event: UmamiEventData | str, event_data: Optional[UmamiEventData] = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            umami.track(event, event_data)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def track_visit(event_data: Optional[UmamiEventData] = None):
    def decorator(func):
        @wraps(func)
        def wrapper(request: HttpRequest, *args, **kwargs):
            new_event_data: UmamiEventData = event_data or UmamiEventData()

            data: UmamiEventData = UmamiEventData(
                url=request.path,
                referrer=request.META.get("HTTP_REFERER", ""),
                title=request.META.get("HTTP_TITLE", ""),
            )

            new_event_data.update(
                {k: v for k, v in data.items() if k not in new_event_data}
            )  # type: ignore[typeddict-item]

            umami.track(new_event_data)
            return func(request, *args, **kwargs)

        return wrapper

    return decorator
