# Decorator Usage

??? abstract "@track"
    === "Event Name"
        === "Description"
            ...
        === "Definition"
            | PARAMETER               | DESCRIPTION                              | REQUIRED                  |
            |-------------------------|------------------------------------------|---------------------------|
            | event  (string)         | The text of the event you'd like to send | :fontawesome-solid-check: |
            | event_data ([UmamiEventData](dataclasses.md#dataclass-umamieventdata-source)) | The data of the event |:fontawesome-solid-x:|

        === "Example"
            !!! example
                ```python
                import django_umami.decorators
                
                @django_umami.decorators.track("Someone called my function!")
                def myview(...)
                    ...
                ```
    === "Event Data"
        === "Description"
            Blah
        === "Definition"
            | PARAMETER                   | DESCRIPTION           | REQUIRED                  |
            |-----------------------------|-----------------------|---------------------------|
            | event  ([UmamiEventData](dataclasses.md#dataclass-umamieventdata-source)) | The data of the event|:fontawesome-solid-check: |
        === "Example"
            !!! example
                ```python
                import django_umami.decorators
                
                @django_umami.decorators.track({"name": "Someone called my view!"})
                def myview(...)
                ```


??? abstract "@track_visit"
    === "Description"
        This will automatically fill in details about your view, e.g. `URL Path`, `Referrer` and `Page Title`.
        You can override any values needed though!
    === "Definition"
        | PARAMETER                   | DESCRIPTION           | REQUIRED                  |
        |-----------------------------|-----------------------|---------------------------|
        | event_data  ([UmamiEventData](dataclasses.md#dataclass-umamieventdata-source)) | The data of the event |:fontawesome-solid-x: |
    === "Example"
        !!! example
            ```python
            import django_umami.decorators
            
            @django_umami.decorators.track_visit()
            def myview(...)
            ```