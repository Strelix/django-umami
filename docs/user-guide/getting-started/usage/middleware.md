# Middleware

## Setup

Add `"django_umami.middleware.TrackAllViewsMiddleware"` to your django settings. Example below.

??? example
    ```python
    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "django_umami.middleware.TrackAllViewsMiddleware" ## ADD THIS LINE
    ]
    ```

And that's it! You are now tracking all views automatically.
> Be aware, this may cause extra latency between requests 
especially if your django server location is far away from the Umami server location.
 

## Settings

Of course, we allow you to modify who you want to track :)



### {==OPTION==} - Filter static

??? abstract "Filter static"
    === "Description"
        Setting this to `True` will block out all requests made to static sources. By default, this is enabled.
    === "Usage"
        ```python
        from django_umami.core import umami
        
        umami.options.filter_static = True
        ```

### {==OPTION==} - Filter media

??? abstract "Filter media"
    === "Description"
        Setting this to `True` will block out all requests made to media sources such as user profile pictures. By default, 
        this is enabled.
    === "Usage"
        ```python
        from django_umami.core import umami
        
        umami.options.filter_media = True
        ```

### {==OPTION==} - Filter anonymous

??? abstract "Filter anonymous"
    === "Description"
        Setting this to `True` will block out all requests made from unauthenticated users. By default, 
        this is disabled and all visits will be tracked.
    === "Usage"
        ```python
        from django_umami.core import umami
        
        umami.options.filter_anonymous = True
        ```

### {==OPTION==} - Filter superuser

??? abstract "Filter superuser"
    === "Description"
        Setting this to `True` will block out all requests made by super users. By default, 
        this is enabled.
    === "Usage"
        ```python
        from django_umami.core import umami
        
        umami.options.filter_superusers = True
        ```
### {==OPTION==} - Filter admin pages

??? abstract "Filter admin pages"
    === "Description"
        Setting this to `True` will block out all requests made to /admin pages. By default, 
        this is disabled.
    === "Usage"
        ```python
        from django_umami.core import umami
        
        umami.options.admin_pages = True
        ```

### {==OPTION==} - Filter custom pages (by path)

??? abstract "Filter custom pages by path"
    === "Description"
        Adding a path to this list will block all tracking for it.
    === "Usage"
        ```python
        from django_umami.core import umami
        
        umami.options.filter_page_paths.append("/dashboard/")
        ```
### {==OPTION==} - Filter custom pages (by URL name)

??? abstract "Filter custom pages by URL name"
    === "Description"
        Adding a URL Name (name="blah" in urls) to this list will block all tracking for it.
    === "Usage"
        ```python
        from django_umami.core import umami
        
        umami.options.filter_page_url_names.append("dashboard")
        ```
