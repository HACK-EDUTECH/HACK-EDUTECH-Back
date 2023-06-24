from django import template

register = template.Library()

@register.filter("key")
def get_by_key(dict_data, key):
    return dict_data.get(key)