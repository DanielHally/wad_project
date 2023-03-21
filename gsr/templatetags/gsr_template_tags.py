from django import template

from gsr.models import Category, RatedModel, Review, Shop

register = template.Library()

@register.inclusion_tag('gsr/tags/render_stars.html')
def render_stars(obj: RatedModel, method: str = RatedModel.OVERALL_RATING):
    """Outputs the star rating for a shop"""

    stars = obj.get_stars(method)
    return {
        'stars' : range(stars),
        'greystars' : range(Review.STARS_MAX - stars),
    }

@register.inclusion_tag('gsr/tags/stars.html')
def star_rating(obj: RatedModel, method: str = RatedModel.OVERALL_RATING):
    """Outputs the star rating for a shop"""

    return {
        'obj' : obj,
        'main_stars' : obj.get_stars(method),
        'methods' : RatedModel.METHODS,
    }

@register.inclusion_tag('gsr/tags/selected.html')
def selected(item_name: str, default_name: str):
    """Outputs `selected="selected"` if the names match"""

    return { 'selected' : item_name == default_name }

MAPS_API_KEY = "AIzaSyAqjZP6ohoMi2IP7xJJ39cM0MnfWt3U_B8"

@register.inclusion_tag('gsr/tags/map_embed.html')
def map_embed(location: str):
    return {
        'key' : MAPS_API_KEY,
        'location' : location
    }

@register.inclusion_tag('gsr/tags/places_lib.html')
def places_lib():
    return {
        'key' : MAPS_API_KEY
    }

@register.inclusion_tag('gsr/tags/picture.html')
def shop_picture(shop: Shop):
    """Gives the url of a shop's picture, or the default"""

    return {
        'obj' : shop,
        'default' : Shop.DEFAULT_PICTURE,
    }

@register.inclusion_tag('gsr/tags/picture.html')
def category_picture(category: Category):
    """Gives the url of a category's picture, or the default"""

    return {
        'obj' : category,
        'default' : Shop.DEFAULT_PICTURE,
    }

@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={'class': css_class})
