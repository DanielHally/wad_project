#!/usr/bin/env python

"""
Populate the database with example data
"""

"""
Setup django
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wad_project.settings')

import django
django.setup()

"""
Main program
"""

from datetime import datetime
from typing import Any, Dict

from django.contrib.auth.models import User, Group

from gsr.models import Category, DatedModel, Shop, Review, ReviewReply

# TODO: pictures
# TODO: reviews, review replies

groups = {
    "Shop Owner": {},
    "Admin": {},
}

users = {
    "Owner 1": {
        'email': "owner1@email.com",
        'groups': ["Shop Owner"],
    },
    "Owner 2": {
        'email': "owner2@email.com",
        'groups': ["Shop Owner"],
    },
    "User 1": {
        'email': "user1@email.com",
    },
    "User 2": {
        'email': "user2@email.com",
    },
}

categories = {
    "Supermarket": {
        'description': "A general supermarket.",
    },
    "Corner Shop": {
        'description': "A corner shop."
    }
}

shops = {
    "The Shop": {
        'description': "It's The Shop.",
        'opening_hours': "Monday-Friday 9-5\nSaturday-Sunday 10-4",
        'location': 'TODO',
        'owners': ["Owner 1"],
        'categories': ["Supermarket"],
    },
    "The Other Shop": {
        'description': "It's not The Shop.",
        'opening_hours': "Wednesday 1-4",
        'location': 'TODO',
        'owners': ["Owner 1", "Owner 2"],
        'categories': ["Corner Shop"],
        'views': 200,
        'date_added': "2022-10-2"
    }
}


def handle_date_added(obj: DatedModel, data: Dict[str, Any]):
    """Set date_added if given for a DatedModel"""

    if 'date_added' in data:
        date = datetime.strptime(data['date_added'], "%Y-%m-%d")
        obj.date_added = date


def add_group(name: str, data: Dict[str, Any]) -> Group:
    """Create a django user group"""

    group = Group.objects.get_or_create(name=name)[0]

    # TODO: permissions?

    group.save()

    return group


def add_user(name: str, data: Dict[str, Any]) -> User:
    """Create a django user"""

    user = User.objects.get_or_create(username=name)[0]
    user.email = data['email']

    for group_name in data.get('groups', []):
        group = Group.objects.get(name=group_name)
        user.groups.add(group)

    user.save()

    return user


def add_category(name: str, data: Dict[str, Any]) -> Category:
    """Create a gsr shop category"""

    category = Category.objects.get_or_create(name=name)[0]
    category.description = data['description']

    category.save()

    return category


def add_shop(name: str, data: Dict[str, Any]) -> Shop:
    """Create a gsr shop"""

    shop = Shop.objects.get_or_create(name=name)[0]
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


def populate():
    """Populate the database with example data"""

    for name, data in groups.items():
        add_group(name, data)
    for name, data in users.items():
        add_user(name, data)
    for name, data in categories.items():
        add_category(name, data)
    for name, data in shops.items():
        add_shop(name, data)


if __name__ == "__main__":
    populate()
