from django.conf import settings


def get_setting(name: str, default=None):
    return getattr(settings, name, default)