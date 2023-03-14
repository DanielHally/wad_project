from django import template

from gsr.models import Shop

register = template.Library()

@register.inclusion_tag('gsr/stars.html')
def star_rating(shop: Shop, method: str = Shop.RatingMethod.OVERALL_RATING):
    return { 'stars' : range(Shop.RatingMethod.methods[method](shop)) }
