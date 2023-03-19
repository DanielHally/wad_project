#!/usr/bin/env python

"""
Populate the database with example data
"""

"""
Setup django
"""

import os

from pytz import utc
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wad_project.settings')

import django
django.setup()

"""
Main program
"""

from typing import Any, Dict

from django.contrib.auth.models import User, Group
from django.utils import timezone

from gsr.models import Category, DatedModel, Shop, Review, ReviewReply

# TODO: pictures

groups = [
    {
        'name': "Shop Owner",
    },
    {
        'name': "Admin",
    },
]

users = [
    {
        'username': "Owner1",
        'email': "owner1@email.com",
        'groups': ["Shop Owner"],
    },
    {
        'username': "Owner2",
        'email': "owner2@email.com",
        'groups': ["Shop Owner"],
    },
    {
        'username': "User1",
        'email': "user1@email.com",
    },
    {
        'username': "User2",
        'email': "user2@email.com",
    },
]

categories = [
    {
        'name': "Supermarket",
        'description': "A general supermarket.",
    },
    {
        'name': "Corner Shop",
        'description': "A corner shop.",
    },
]

shops = [
    {
        'name': "The Shop",
        'description': "It's The Shop.",
        'opening_hours': "Monday-Friday 9-5\nSaturday-Sunday 10-4",
        'location': 'ChIJozqrTldFiEgRcnQtvvM7kUA',
        'owners': ["Owner1"],
        'categories': ["Supermarket"],
        'date_added': "2020-10-2",
    },
    {
        'name': "The Other Shop",
        'description': "It's not The Shop.",
        'opening_hours': "Wednesday 1-4",
        'location': 'ChIJ-4qF7s5FiEgR6bRXbXOZeek',
        'owners': ["Owner1", "Owner2"],
        'categories': ["Corner Shop"],
        'views': 200,
    }
]

reviews = [
    {
        'id': 1,
        'shop': "The Shop",
        'author': "Owner1",
        'customer_interaction_rating': 5,
        'price_rating': 1,
        'quality_rating': 1,
        'comment': "Owner is a very nice person.",
        'date_added': "2021-9-12"
    },
    {
        'id': 2,
        'shop': "The Shop",
        'author': "Owner2",
        'customer_interaction_rating': 1,
        'price_rating': 4,
        'quality_rating': 3,
    },
    {
        'id': 3,
        'shop': "The Shop",
        'author': "User1",
        'customer_interaction_rating': 4,
        'price_rating': 2,
        'quality_rating': 5,
        'comment': "Very good quality products, quite pricy."
    },
    {
        'id' : 4,
        'shop' : "The Other Shop",
        'author' : "User1",
        'customer_interaction_rating' : 5,
        'price_rating' : 1,
        'quality_rating' : 1,
    }
]

review_replies = [
    {
        'id': 1,
        'review': 1,
        'author': "Owner2",
        'comment': "Maybe",
    },
    {
        'id': 2,
        'review': 1,
        'author': "Owner1",
        'comment': "Yes",
    },
    {
        'id': 3,
        'review': 3,
        'author': "User2",
        'comment': "I agree",
    }
]


def handle_date_added(obj: DatedModel, data: Dict[str, Any]):
    """Set date_added if given for a DatedModel"""

    if 'date_added' in data:
        date = timezone.datetime.strptime(data['date_added'], "%Y-%m-%d").replace(tzinfo=utc)
        obj.date_added = date


def add_group(data: Dict[str, Any]) -> Group:
    """Create a django user group"""

    group = Group.objects.get_or_create(name=data['name'])[0]

    # TODO: permissions?

    group.save()

    return group


def add_user(data: Dict[str, Any]) -> User:
    """Create a django user"""

    user = User.objects.get_or_create(username=data['username'])[0]
    user.email = data['email']

    for group_name in data.get('groups', []):
        group = Group.objects.get(name=group_name)
        user.groups.add(group)

    user.save()

    return user


def add_category(data: Dict[str, Any]) -> Category:
    """Create a gsr shop category"""

    category = Category.objects.get_or_create(name=data['name'])[0]
    category.description = data['description']

    category.save()

    return category


def add_shop(data: Dict[str, Any]) -> Shop:
    """Create a gsr shop"""

    shop = Shop.objects.get_or_create(name=data['name'])[0]
    shop.description = data.get('description', "")
    shop.opening_hours = data['opening_hours']
    shop.location = data['location']

    for category_name in data.get('categories', []):
        category = Category.objects.get(name=category_name)
        shop.categories.add(category)

    for owner_name in data['owners']:
        owner = User.objects.get(username=owner_name)
        shop.owners.add(owner)

    shop.views = data.get('views', 0)

    handle_date_added(shop, data)

    shop.save()

    return shop


def add_review(data: Dict[str, Any]) -> Review:
    """Create a gsr review"""

    review = Review.objects.get_or_create(
        id=data['id'],
        defaults={
            'customer_interaction_rating': data['customer_interaction_rating'],
            'price_rating': data['price_rating'],
            'quality_rating': data['quality_rating'],
            'shop': Shop.objects.get(name=data['shop']),
            'author': User.objects.get(username=data['author']),
            'comment': data.get('comment', ""),
        }
    )[0]

    handle_date_added(review, data)

    review.save()

    return review


def add_review_reply(data: Dict[str, Any]) -> ReviewReply:
    """Create a gsr review reply"""

    reply = ReviewReply.objects.get_or_create(
        id=data['id'],
        defaults={
            'review': Review.objects.get(id=data['review']),
            'author': User.objects.get(username=data['author']),
            'comment': data['comment'],
        }
    )[0]

    handle_date_added(reply, data)

    reply.save()

    return reply


def populate():
    """Populate the database with example data"""

    for data in groups:
        add_group(data)
    for data in users:
        add_user(data)
    for data in categories:
        add_category(data)
    for data in shops:
        add_shop(data)
    for data in reviews:
        add_review(data)
    for data in review_replies:
        add_review_reply(data)


if __name__ == "__main__":
    populate()
