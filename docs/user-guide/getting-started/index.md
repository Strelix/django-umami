# Quick Start


Install:

```shell
pip install django-umami
```

Use as a decorator for your django view:
```python
import django_umami.decorators

@django_umami.decorators.track("my custom event!")
def myview(request):
    ...
```

Or use standalone:
```python
import django_umami.core

def myview(request):
    django_umami.core.umami.track("someone went to django view!")
    ...
```


## Content

- [Installation](installation.md)
- [Settings](settings.md)
- [Usage](usage/core.md)