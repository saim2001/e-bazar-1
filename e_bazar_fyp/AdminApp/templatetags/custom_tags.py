# custom_tags.py
from django import template

register = template.Library()


def get_range(value):
    return range(len(value))

def index(indexable, i):
    return indexable[i]


register.filter('get_range', get_range)
register.filter('index', index)