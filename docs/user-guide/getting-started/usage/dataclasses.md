??? info "NOTE: Basic Usage"
    To use a dataclass, you can either use it directly or by using a dictionary.
    
    ```python
    Umami(UmamiConfig(enabled=True))
    
    # or

    Umami({"enabled": True})
    ```

    It's up to you. But with an IDE such as one from JetBrains you'll get these type hints even for dictionaries.


## {==Dataclass==} - UmamiConfig <sub><sup>([Source](https://github.com/TreyWW/django-umami/blob/master/django_umami/core.py#L16))</sup></sub>

??? abstract "Class - UmamiConfig"
    === "Definition"
        | PARAMETER  | DATA TYPE        | EXAMPLE                             | DESCRIPTION                                                                                                                | REQUIRED                  |
        |------------|------------------|-------------------------------------|----------------------------------------------------------------------------------------------------------------------------|---------------------------|
        | enabled    | boolean          | True                                | Whether django_umami should be enabled. This is good to temporarily turn off tracking without removing all decorators etc. | :fontawesome-solid-check: |
        | host_url   | string           | "https://mysite.com/"               | The main URL where your umami is hosted. The BASE url **NOT** including anything like `script.js` or `/api/send`           | :fontawesome-solid-check: |
        | website_id | string (uuid)    | "a123b4c5-xxxx-xxxx-xxxx-xxxxxxxxx" | The website ID of the website object in Umami. Go to Websites -> Edit to copy the ID.                                      | :fontawesome-solid-check: |
        | session    | requests.Session | | Don't add to this manually, use `create_session()` to create the session.                                                  | :fontawesome-solid-x:     |
    === "Methods"
        | NAME           | PARAMETERS          | DESCRIPTION                                                                                                                                    |
        |----------------|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------|
        | create_session |                     | Used to create a session that will allow requests to your Umami server to be made much faster.                                                 |
        | close_session  |                     | This will close any active session Umami is using.                                                                                             |
        | set_enabled    | enabled (bool)      | Sets the value of enabled to whatever you pass in. This will enable/disable django_umami. Django will still perform normally even if disabled. |
        | set_host_url   | host_url (string)   | Sets the value of host_url to whatever you pass in. This will globally set it for all future calls.                                            |
        | set_website_id | website_id (string) | Sets the value of website_id to whatever you pass in. This will globally change the website ID for all future calls.                           |


## {==Dataclass==} - UmamiEventData <sub><sup>([Source](https://github.com/TreyWW/django-umami/blob/master/django_umami/core.py#L38))</sup></sub>

??? abstract "Class - UmamiConfig"
    | PARAMETER | DATA TYPE | EXAMPLE                     | REQUIRED              |
    |-----------|-----------|-----------------------------|-----------------------|
    | hostname  | string    | "My Host"                   | :fontawesome-solid-x: |
    | language  | string    | "en-GB"                     | :fontawesome-solid-x: |
    | referrer  | string    | "https://example.com"       | :fontawesome-solid-x: |
    | screen    | string    | "1920x1080"                 | :fontawesome-solid-x: |
    | title     | string    | "my site \| Page One"       | :fontawesome-solid-x: |
    | url       | string    | "/page1/blob/               | :fontawesome-solid-x: |
    | name      | string    | "Someone visited my site!?" | :fontawesome-solid-x: |

## {==Dataclass==} - UmamiPayload <sub><sup>([Source](https://github.com/TreyWW/django-umami/blob/master/django_umami/core.py#L49))</sup></sub>

??? abstract "Class - UmamiPayload"
    === "Definition"
        | PARAMETER | DATA TYPE      | EXAMPLE                | REQUIRED                  |
        |-----------|----------------|------------------------|---------------------------|
        | website   | str            | "xxxxx-xxxx-xxxx-xxxx" | :fontawesome-solid-check: |
        | data      | UmamiEventData | {"name": "blob"}       | :fontawesome-solid-x:     |
    === "Usage"
        ```python
        import django_umamo.core
        
        payload = django_umami.core.UmamiPayload(website="xyz")
        payload = {"website": "xyz"}
        ```

## {==Main Class==} - Umami <sub><sup>([Source](https://github.com/TreyWW/django-umami/blob/master/django_umami/core.py#L61))</sup></sub>


??? abstract "Main Class - Umami"
    === "Definition"
        | PARAMETER | DATA TYPE       | EXAMPLE                | REQUIRED                  |
        |-----------|-----------------|------------------------|---------------------------|
        | options   | [UmamiConfig](#dataclass-umamiconfig-source) | {"enabled": True, ...} | :fontawesome-solid-check: |
    === "Methods"
        | NAME                   | INFO                                                        | RETURNS       |
        |------------------------|-------------------------------------------------------------|---------------|
        | check_website_settings | Used to check if settings are valid and should send request | bool          |
        | send                   | Used to send raw request                                    |               |
        | track                  | Used to send tracking events (wrapper around send)          | UmamiResponse |
        | track_event_name       | Used to send just an event name (wrapper around send)       | UmamiResponse |
    === "Usage"
        ```python
        import django_umamo.core
        
        django_umami.core.umami.check_website_settings()
        ```