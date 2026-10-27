"""Version local assets so normal refreshes always load their current content."""
from pathlib import Path
from django import template
from django.conf import settings
from django.templatetags.static import static

register=template.Library()

@register.simple_tag
def asset(path):
    url=static(path)
    local=Path(settings.BASE_DIR)/'static'/path
    if local.is_file():
        stat=local.stat()
        return url+'?v='+str(stat.st_mtime_ns)+'-'+str(stat.st_size)
    return url
