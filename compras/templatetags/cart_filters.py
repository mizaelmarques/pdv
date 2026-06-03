from django import template


register = template.Library()


@register.filter
def get_item(dictionary, key):
    try:
        for item in dictionary:
            if item.id == int(key):
                return item
    except:
        pass
    return None


@register.filter
def mul(value, arg):
    return value * arg
