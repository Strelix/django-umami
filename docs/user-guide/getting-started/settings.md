# Settings

To use django-umami efficiently, it's best to configure it exactly to your needs, right!
To do this you can use either use environment variables or manually call the methods.

## Using environment variables

```dotenv title=".env"
UMAMI_PAGE_URL=https://mysite.com
UMAMI_WEBSITE_ID=1234-1234-1234
UMAMI_TRACKING_ENABLED=True
```

## Using umami object

!!! tip

    Make sure to import any files needed first!
    === "Core"
        ```python
        import django_umami.core

        django_umami.core.umami.options...
        ```
    === "Decorators"
        ```python
        import django_umami.decorators
        
        @django_umami.decorators...
        ```
    === "Only what you need"
        ```python
        from django_umami.core import umami

        umami.options...
        ```

### {==Method==} - Set Host URL

!!! abstract "Set Host URL"
    === "Description"
        This allows you to set the main host URL of umami. This is only required if you have not set it via the `UMAMI_PAGE_URL` 
        environment variable.
    === "Definition"
        | PARAMETER  | DESCRIPTION                                               | REQUIRED                  |
        |------------|-----------------------------------------------------------|---------------------------|
        | host_url  _(string)_ | Your analytics site url E.g. `https://mysite.com` | :fontawesome-solid-check: |
    === "Usage"
        ```python
        from django_umami.core import umami
        
        umami.options.set_host_url("https://example.com")
        ```


### {==Method==} - Set Website ID

!!! abstract "Set Website ID"
    === "Description"
        This allows you to set the main host URL of umami. This is only required if you have not set it via the `UMAMI_WEBSITE_ID` 
        environment variable.
    === "Definition"
        | PARAMETER  | DESCRIPTION                               | REQUIRED                  |
        |------------|-------------------------------------------|---------------------------|
        | website_id  _(string - uuid)_ | Your website id E.g. `12345678-12345....` | :fontawesome-solid-check: |
    === "Usage"
        ```python
        from django_umami.core import umami
        
        umami.options.set_website_id("123456")
        ```

### {==Method==} - Create Session

!!! tip "Using Sessions"
    === "Description"
        Sessions allow for requests to your Umami server to be streamed in one session. This allows for requests to take 
        around a third of the time a standard request would take!
    === "Usage"
        ```python
        from django_umami.core import umami
        
        umami.options.create_session()
        ```
