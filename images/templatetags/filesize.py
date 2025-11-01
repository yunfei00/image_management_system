# templatetags/filesize.py
from django import template
register = template.Library()

@register.filter
def filesize_fmt(num):
    for unit in ['B','KB','MB','GB','TB']:
        if num < 1024:
            return f"{num:.2f} {unit}" if unit != 'B' else f"{num} {unit}"
        num /= 1024
    return f"{num:.2f} PB"
