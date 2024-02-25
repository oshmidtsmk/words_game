from django import template

register = template.Library()

@register.filter
def group_by(queryset, attribute):
    """
    takes a queryset and an attribute as input
    and groups the queryset elements by the specified attribute.
    """
    grouped_data = {}
    for item in queryset:
        key = getattr(item, attribute) # Gets the value of the specified attribute for the current item.
        grouped_data[key] = grouped_data.get(key, 0) + 1 #Updates the dictionary by incrementing the count for the current key.
    return grouped_data
