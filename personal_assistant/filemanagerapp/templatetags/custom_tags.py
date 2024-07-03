from django import template

register = template.Library()


@register.filter
def translate_category(category_name, translated_categories):
    return translated_categories.get(category_name, category_name)
