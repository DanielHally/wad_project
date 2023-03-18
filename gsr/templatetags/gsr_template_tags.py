from django import template

from gsr.models import RatedModel, Review

register = template.Library()

@register.inclusion_tag('gsr/tags/stars.html')
def star_rating(obj: RatedModel, method: str = RatedModel.OVERALL_RATING):
    """Outputs the star rating for a shop"""

    stars = obj.get_stars(method)
    return {
        'stars' : range(stars),
        'greystars' : range(Review.STARS_MAX - stars),
    }

@register.inclusion_tag('gsr/tags/selected.html')
def selected(item_name: str, default_name: str):
    """Outputs `selected="selected"` if the names match"""

    return { 'selected' : item_name == default_name }

@register.inclusion_tag('gsr/tags/map_embed.html')
def map_embed(location: str):
    return {
        'key' : "AIzaSyAqjZP6ohoMi2IP7xJJ39cM0MnfWt3U_B8",
        'location' : location
    }
