from functools import wraps

from django_umami.core import umami, UmamiEventData


def track(event_name: str, event_data: UmamiEventData = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            umami.track(event_name, event_data)
            return func(*args, **kwargs)

        return wrapper

    return decorator
