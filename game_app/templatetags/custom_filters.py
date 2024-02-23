from django import template

register = template.Library()

@register.filter
def group_by(queryset, attribute):
    grouped_data = {}
    for item in queryset:
        key = getattr(item, attribute)
        grouped_data[key] = grouped_data.get(key, 0) + 1
    return grouped_data
