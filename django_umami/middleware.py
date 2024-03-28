import logging

from django_umami.core import umami

class TrackAllViewsMiddleware:
    def __init__(self, get_response):
        print("init?")
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if self._allowed_to_track(request):
            logging.debug(f"Tracking {request.path}")
            umami.track({
                "url": request.path,
                "referrer": request.META.get("HTTP_REFERER"),
                "hostname": request.META.get("SERVER_NAME"),
            })
        return response

    def _allowed_to_track(self, request):
        if not hasattr(request, "session"):
            logging.critical("To use the TrackAllViewsMiddleware you need to have 'django.contrib.sessions.middleware.SessionMiddleware' "
                             "in django settings 'MIDDLEWARE'")
            return False
        if (
            request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        ):
            return False
        return True