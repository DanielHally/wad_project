#!/usr/bin/env python

"""
Populate the database with example data
"""

"""
Setup django
"""

import os
from shutil import copy

from pytz import utc

from wad_project.settings import MEDIA_ROOT, STATIC_DIR
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wad_project.settings')

import django
django.setup()

"""
Main program
"""

from typing import Any, Dict

from django.contrib.auth.models import Group, Permission, User 
from django.utils import timezone

from gsr.models import Category, DatedModel, Shop, Review, ReviewReply

groups = [
    {
        'name': "Shop Owner",
        'permissions': ["manage_shops"],
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
    {
        'username': "Tycoon",
        'email': "money@underpaidworkers.com",
        'groups': ["Shop Owner"],
    },
    {
        'username': "smallbuisnessowner",
        'email': "community@caredforworkers.com",
        'groups': ["Shop Owner"],
    },
    {
        'username': "anotherbloodyowner",
        'email': "owner@again.com",
        'groups': ["Shop Owner"],
    },
    {
        'username': "themanwhoowns",
        'email': "owner@inveitable.com",
        'groups': ["Shop Owner"],
    },
    {
        'username': "shoppermannn",
        'email': "likesshopping@markets.com",
    },
    {
        'username': "buyerofthings",
        'email': "purchesersof@shops.com",
    },
    {
        'username': "itembuyer",
        'email': "shopperman@shops.com",
    },
]

categories = [
    {
        'name': "Supermarket",
        'picture' : "supermarket.png",
        'description': "A general supermarket.",
        'is_approved' : True,
    },
    {
        'name': "Corner Shop",
        'picture' : "corner_shop.png",
        'description': "A corner shop.",
        'is_approved' : True,
    },
]

shops = [
    {
        'name': "The Shop",
        'picture': "the_shop.png",
        'description': "It's The Shop.",
        'opening_hours': "Monday-Friday 9-5\nSaturday-Sunday 10-4",
        'location': 'ChIJozqrTldFiEgRcnQtvvM7kUA',
        'owners': ["Owner1"],
        'categories': ["Supermarket"],
        'date_added': "2020-10-2",
        'reviews' : [
            {
                'id': 1,
                'author': "Owner1",
                'customer_interaction_rating': 5,
                'price_rating': 1,
                'quality_rating': 1,
                'comment': "Owner is a very nice person.",
                'date_added': "2021-9-12"
            },
            {
                'id': 2,
                'author': "Owner2",
                'customer_interaction_rating': 1,
                'price_rating': 4,
                'quality_rating': 3,
            },
            {
                'id': 3,
                'author': "User1",
                'customer_interaction_rating': 4,
                'price_rating': 2,
                'quality_rating': 5,
                'comment': "Very good quality products, quite pricy."
            },    
        ]
    },
    {
        'name': "The Other Shop",
        'picture': "the_other_shop.png",
        'description': "It's not The Shop.",
        'opening_hours': "Wednesday 1-4",
        'location': 'ChIJ-4qF7s5FiEgR6bRXbXOZeek',
        'owners': ["Owner1", "Owner2"],
        'categories': ["Corner Shop"],
        'views': 200,
        'reviews' : [
            {
                'id' : 4,
                'shop' : "The Other Shop",
                'author' : "User1",
                'customer_interaction_rating' : 5,
                'price_rating' : 1,
                'quality_rating' : 1,
            },
        ]
    },
        {
        'name': "Pantryplus",
        'picture': "the_other_shop.png",
        'description': "Sells plenty of pantry filling items. Fun for the whole family",
        'opening_hours': "Monday-Friday 9-5\nSaturday-Sunday 10-4",
        'location': 'ChIJiSKpi8xFiEgRPgcHFo1WdRI',
        'owners': ["Owner1", "Owner2"],
        'categories': ["Corner Shop"],
        'views': 200,
        'reviews' : [
            {
                'id' : 5,
                'shop' : "Pantryplus",
                'author' : "itembuyer",
                'customer_interaction_rating' : 3,
                'price_rating' : 3,
                'quality_rating' : 3,
            },
            {
                'id' : 6,
                'shop' : "Pantryplus",
                'author' : "itembuyer",
                'customer_interaction_rating' : 4,
                'price_rating' : 4,
                'quality_rating' : 4,
            },
            {
                'id' : 7,
                'shop' : "Pantryplus",
                'author' : "itembuyer",
                'customer_interaction_rating' : 5,
                'price_rating' : 5,
                'quality_rating' : 5,
            }]
    },
        {
        'name': "Jimmies",
        'picture': "the_other_shop.png",
        'description': "This is Jimmies cornershop not to be mistaken with Jimmy's cornershop",
        'opening_hours': "Monday-Friday 9-5\nSaturday-Sunday 10-4",
        'location': 'ChIJAzLzcsxFiEgRjTjT96NloVA',
        'owners': ["Tycoon"],
        'categories': ["Corner Shop"],
        'views': 86,
        'reviews' : [
            {
                'id' : 8,
                'shop' : "Jimmies",
                'author' : "itembuyer",
                'customer_interaction_rating' : 3,
                'price_rating' : 3,
                'quality_rating' : 3,
                
            },{
                'id' : 9,
                'shop' : "Jimmies",
                'author' : "itembuyer",
                'customer_interaction_rating' : 4,
                'price_rating' : 4,
                'quality_rating' : 4,
            },{
                'id' : 10,
                'shop' : "Jimmies",
                'author' : "itembuyer",
                'customer_interaction_rating' : 5,
                'price_rating' : 5,
                'quality_rating' : 5,
            }
        ]
    },
    {
        'name': "Jimmy's",
        'picture': "the_other_shop.png",
        'description': "This is Jimmy's cornershop not to be mistaken with Jimmies cornershop",
        'opening_hours': "Monday-Friday 9-5\nSaturday-Sunday 10-4",
        'location': ' ChIJv3iNt8NFiEgRbbHwZjXzhW4',
        'owners': ["themanwhoowns"],
        'categories': ["Corner Shop"],
        'views': 46,
        'reviews' : [
            {
                'id' : 11,
                'shop' : "Jimmy's",
                'author' : "itembuyer",
                'customer_interaction_rating' : 3,
                'price_rating' : 3,
                'quality_rating' : 3,
                },{
                'id' : 12,
                'shop' : "Jimmy's",
                'author' : "itembuyer",
                'customer_interaction_rating' : 4,
                'price_rating' : 4,
                'quality_rating' : 4,}
                ,{
                'id' : 13,
                'shop' : "Jimmy's",
                'author' : "itembuyer",
                'customer_interaction_rating' : 5,
                'price_rating' : 5,
                'quality_rating' : 5,
            },
        ]
    },
    {
        'name': "shoppy mc shop face",
        'picture': "the_other_shop.png",
        'description': "This shop was named by the British public.",
        'opening_hours': "Wednesday 1-4\nTuesday 7-7\n Friday 5-6",
        'location': 'ChIJ8cF-6MtFiEgRwMvh3DDvPDY',
        'owners': ["Tycoon"],
        'categories': ["Supermarket"],
        'views': 15,
        'reviews' : [
            {
                'id' : 22,
                'shop' : "shoppy mc shop face",
                'author' : "User1",
                'customer_interaction_rating' : 5,
                'price_rating' : 1,
                'quality_rating' : 1,
            },
        ]
    },
    {
        'name': "bingobango",
        'picture': "the_other_shop.png",
        'description': "The only place your heart desires",
        'opening_hours': "24 Hour Shop",
        'location': 'ChIJ8cF-6MtFiEgRwMvh3DDvPDY',
        'owners': ["Tycoon"],
        'categories': ["Supermarket"],
        'views': 15,
        'reviews' : [
            {
                'id' : 21,
                'shop' : "bingobango",
                'author' : "User1",
                'customer_interaction_rating' : 5,
                'price_rating' : 1,
                'quality_rating' : 1,
            },
        ]
    },
    {
        'name': "El Salvador's",
        'picture': "the_other_shop.png",
        'description': "Rises in the east.",
        'opening_hours': "24 Hour Shop",
        'location': 'ChIJBa5oLsxFiEgR-TLrAGrNBDo',
        'owners': ["Tycoon"],
        'categories': ["Supermarket"],
        'views': 1500,
        'reviews' : [
            {
                'id' : 20,
                'shop' : "El Salvador's",
                'author' : "User1",
                'customer_interaction_rating' : 5,
                'price_rating' : 1,
                'quality_rating' : 1,
            },
        ]
    },
    {
        'name': "Spicy Tortailini",
        'picture': "the_other_shop.png",
        'description': "Sponsored by Matteo Campinille",
        'opening_hours': "Wednesday 8-8",
        'location': 'ChIJk8sA985FiEgRiBNqStymKBs',
        'owners': ["Tycoon"],
        'categories': ["Supermarket"],
        'views': 12,
        'reviews' : [
            {
                'id' : 19,
                'shop' : "Spicy Tortailini",
                'author' : "User1",
                'customer_interaction_rating' : 5,
                'price_rating' : 1,
                'quality_rating' : 1,
            },
        ]
    },
    {
        'name': "Door Dash",
        'picture': "the_other_shop.png",
        'description': "Doors direct to your doors",
        'opening_hours': "Sunday 1-3",
        'location': 'ChIJk8sA985FiEgRiBNqStymKBs',
        'owners': ["anotherbloodyowner"],
        'categories': ["Supermarket"],
        'views': 20000,
        'reviews' : [
            {
                'id' : 18,
                'shop' : "Door Dash",
                'author' : "User1",
                'customer_interaction_rating' : 5,
                'price_rating' : 1,
                'quality_rating' : 1,
            },
        ]
    },
    {
        'name': "Deadeye",
        'picture': "the_other_shop.png",
        'description': "We defintely dont sell illegal firearms",
        'opening_hours': "Wednesday 9-9",
        'location': 'ChIJH81g3A1FiEgRUm8QVTFC5_M',
        'owners': ["anotherbloodyowner"],
        'categories': ["Supermarket"],
        'views': 4,
        'reviews' : [
            {
                'id' : 17,
                'shop' : "Deadeye",
                'author' : "User1",
                'customer_interaction_rating' : 5,
                'price_rating' : 1,
                'quality_rating' : 1,
            },
        ]
    },
    {
        'name': "Funky Monkey",
        'picture': "the_other_shop.png",
        'description': "Not horsing arounds",
        'opening_hours': "Wednesday 9-9\nFriday 12-6",
        'location': 'ChIJH81g3A1FiEgRUm8QVTFC5_M',
        'owners': ["anotherbloodyowner"],
        'categories': ["Corner Shop"],
        'views': 4,
        'reviews' : [
            {
                'id' : 14,
                'shop' : "Funky Monkey",
                'author' : "itembuyer",
                'customer_interaction_rating' : 1,
                'price_rating' : 1,
                'quality_rating' : 1,
            },
        ]
    },
    {
        'name': "No Porkin",
        'picture': "the_other_shop.png",
        'description': "No Porkin",
        'opening_hours': "Wednesday 9-9\nFriday 12-6\nSaturday 4-3",
        'location': 'ChIJz11hvC9FiEgRc8ifQ5FWBtM',
        'owners': ["anotherbloodyowner"],
        'categories': ["Corner Shop"],
        'views': 1000000000,
        'reviews' : [
            {
                'id' : 15,
                'shop' : "No Porkin",
                'author' : "itembuyer",
                'customer_interaction_rating' : 1,
                'price_rating' : 1,
                'quality_rating' : 1,
            },
        ]
    },
    {
        'name': "Dog Food",
        'picture': "the_other_shop.png",
        'description': "I wonder what you can buy here.... Only cat food",
        'opening_hours': "Wednesday 9-9\nFriday 12-6\nSaturday 4-3",
        'location': 'ChIJ-TPET55FiEgR2pWRz4zRxgs',
        'owners': ["anotherbloodyowner"],
        'categories': ["Corner Shop"],
        'views': 10000,
        'reviews' : [
            {
                'id' : 16,
                'shop' : "Dog Food",
                'author' : "User1",
                'customer_interaction_rating' : 4,
                'price_rating' : 1,
                'quality_rating' : 5,
            },
        ]
    }]

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


def add_picture(path: str, upload_to: str) -> str:
    """Copies a file from /static/population_images/ to /media/"""

    # Build paths
    relative = upload_to + '/' + path
    dest = os.path.join(MEDIA_ROOT, upload_to)

    # Make folders if needed
    os.makedirs(dest, exist_ok=True)

    # Copy file to media
    copy(
        os.path.join(STATIC_DIR, 'population_images', path),
        dest
    )

    # Return relative path
    return relative


def handle_date_added(obj: DatedModel, data: Dict[str, Any]):
    """Set date_added if given for a DatedModel"""

    if 'date_added' in data:
        date = timezone.datetime.strptime(data['date_added'], "%Y-%m-%d").replace(tzinfo=utc)
        obj.date_added = date


def add_group(data: Dict[str, Any]) -> Group:
    """Create a django user group"""

    group = Group.objects.get_or_create(name=data['name'])[0]
    for perm_name in data['permissions']:
        perm = Permission.objects.get(codename=perm_name)
        group.permissions.add(perm)

    group.save()

    return group


def add_user(data: Dict[str, Any]) -> User:
    """Create a django user"""

    user = User.objects.get_or_create(username=data['username'])[0]
    user.email = data['email']
    user.set_password(user.username)

    for group_name in data.get('groups', []):
        group = Group.objects.get(name=group_name)
        user.groups.add(group)

    user.save()

    return user


def add_category(data: Dict[str, Any]) -> Category:
    """Create a gsr shop category"""

    category = Category.objects.get_or_create(name=data['name'])[0]
    category.description = data['description']

    category.is_approved = data['is_approved']
    if 'picture' in data:
        category.picture.name = add_picture(data['picture'], Category.MEDIA_SUBDIR)


    category.save()

    return category


def add_shop(data: Dict[str, Any]) -> Shop:
    """Create a gsr shop"""

    shop = Shop.objects.get_or_create(name=data['name'])[0]
    shop.description = data.get('description', "")
    shop.opening_hours = data['opening_hours']
    shop.location = data['location']
    if 'picture' in data:
        shop.picture.name = add_picture(data['picture'], Shop.MEDIA_SUBDIR)

    for category_name in data.get('categories', []):
        category = Category.objects.get(name=category_name)
        shop.categories.add(category)

    for owner_name in data['owners']:
        owner = User.objects.get(username=owner_name)
        shop.owners.add(owner)

    for review in data['reviews']:
        add_review(shop, review)

    shop.views = data.get('views', 0)

    handle_date_added(shop, data)

    shop.save()

    return shop


def add_review(shop: Shop, data: Dict[str, Any]) -> Review:
    """Create a gsr review"""

    review = Review.objects.get_or_create(
        id=data['id'],
        defaults={
            'customer_interaction_rating': data['customer_interaction_rating'],
            'price_rating': data['price_rating'],
            'quality_rating': data['quality_rating'],
            'shop': shop,
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
    for data in review_replies:
        add_review_reply(data)


if __name__ == "__main__":
    populate()
