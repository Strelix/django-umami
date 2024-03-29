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
        # if not hasattr(request, "session"):
        #     logging.critical("To use the TrackAllViewsMiddleware you need to have 'django.contrib.sessions.middleware.SessionMiddleware' "
        #                      "in django settings 'MIDDLEWARE'")
        #     return False
        if umami.options.filter_htmx and request.htmx:
            return False
        if umami.options.filter_static and request.path.startswith("/static"):
            return False
        if umami.options.filter_admin_pages and request.path.startswith("/admin"):
            return False
        if umami.options.filter_media and request.path.startswith("/media"):
            return False
        if umami.options.filter_anonymous and (not request.user or request.user.is_anonymous):
            return False
        if umami.options.filter_superusers and (not request.user or not request.user.is_superuser):
            return False

        if request.path in umami.options.filter_page_paths:
            return False

        if request.resolver_match.url_name in umami.options.filter_page_url_names:
            return False

        return True
