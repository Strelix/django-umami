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
