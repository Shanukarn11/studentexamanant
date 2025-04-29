from django import template
register = template.Library()

@register.filter
def to(start, end):
    return range(start, end + 1)

@register.filter
def get_question(obj, num):
    return getattr(obj, f'q{num}', None)