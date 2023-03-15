from django import template

from gsr.models import Shop

register = template.Library()

@register.inclusion_tag('gsr/stars.html')
def star_rating(shop: Shop, method: str = Shop.RatingMethod.OVERALL_RATING):
    """Outputs the star rating for a shop"""

    return { 'stars' : range(Shop.RatingMethod.methods[method](shop)) }

@register.inclusion_tag('gsr/selected.html')
def selected(item_name: str, default_name: str):
    """Outputs `selected="selected"` if the names match"""

    return { 'selected' : item_name == default_name }
