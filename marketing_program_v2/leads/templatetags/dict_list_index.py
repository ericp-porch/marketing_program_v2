from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def dict_list_index(context, dict, key, index):
    return dict[key][index]

