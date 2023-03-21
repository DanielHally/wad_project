from datetime import timedelta
from typing import List

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone
from pytz import utc

from gsr.models import RatedModel, Review, Shop

def to_query_set_strs(list):
    return [
        f"<{type(elem).__name__}: {elem}>"
        for elem in list
    ]

class DatedModelUtils:
    """Helpers for DatedModelTests"""

    """A time in the past"""
    PAST = timezone.datetime(2000, 1, 1, tzinfo=utc)
        

    @staticmethod
    def make_new() -> Shop:
        """Creates a Shop as an example of a dated model with a modern date_updated"""

        ret = Shop(
            name="Shop",
            description="Shop desc",
            opening_hours="Opening hours",
            location="TODO",
        )
        ret.save()

        return ret

    @staticmethod
    def make_old() -> Shop:
        """Creates a Shop as an example of a dated model with the date_updated in the past"""

        # Create initial model
        model = DatedModelUtils.make_new()

        # Set time updated to the past
        model.date_updated = DatedModelUtils.PAST
        model.save()

        return model

    @staticmethod
    def trigger_update(model: Shop):
        """Triggers a date_updated change for a shop"""

        model.name = model.name + " changed"
        model.save()

class DatedModelTests(TestCase):
    """Tests for DatedModel, using Shop as an example implementation"""

    def test_new_date_added(self):
        """Test that date added is set for a new object"""

        model = DatedModelUtils.make_new()
        self.assertLessEqual(
            timezone.now() - model.date_added,
            timedelta(minutes=5)
        )

    def test_new_date_updated(self):
        """Test that date updated is set for a new object"""

        model = DatedModelUtils.make_new()
        self.assertLessEqual(timezone.now().day - model.date_updated.day, 1)

    def test_old_date_writeable(self):
        """Test that date updated is writeable for an object"""

        model = DatedModelUtils.make_old()
        self.assertEqual(DatedModelUtils.PAST, model.date_updated)

    def test_old_date_updated(self):
        """Test that date updated is set for an old object with changes"""

        model = DatedModelUtils.make_old()
        DatedModelUtils.trigger_update(model)
        self.assertLessEqual(
            timezone.now() - model.date_added,
            timedelta(minutes=5)
        )
    
    # TODO: test non-dated fields

class ReviewUtils:
    """Helpers for ReviewTest"""

    """Data to make example reviews from"""
    rating_data = [
        {
            "customer_interaction_rating" : 5,
            "price_rating" : 5,
            "quality_rating" : 5,
        },
        {
            "customer_interaction_rating" : 4,
            "price_rating" : 4,
            "quality_rating" : 4,
        },
        {
            "customer_interaction_rating" : 4,
            "price_rating" : 3,
            "quality_rating" : 1,
        }
    ]

    """Expected overall ratings for the example reviews"""
    expected_overall = [
        5,
        4,
        8/3
    ]

    """Expected overall ratings for a shop with the example reviews"""
    expected_stars = 4

    @staticmethod
    def get_user() -> User:
        author = User.objects.get_or_create(username="Author")[0]
        return author

    @staticmethod
    def make_examples(shop=None) -> List[Review]:
        """Makes a group of example reviews"""

        # Make a default shop if needed
        if shop is None:
            shop = Shop()
            shop.save()
        
        # Make an author user
        author = ReviewUtils.get_user()

        # Create reviews from data
        ret = []
        for entry in ReviewUtils.rating_data:
            review = Review(**entry, shop=shop, author=author)
            review.save()
            ret.append(review)

        return ret
    
    @staticmethod
    def make_with_rating(shop, rating):
        review = Review(
            shop=shop,
            author=ReviewUtils.get_user(),
            customer_interaction_rating=rating,
            price_rating=rating,
            quality_rating=rating,
        )
        review.save()
        return review

class ReviewTest(TestCase):
    """Tests for Review"""

    def test_overall_rating(self):
        """Checks the overall rating of a Review works"""

        reviews = ReviewUtils.make_examples()

        for i, review in enumerate(reviews):
            self.assertEqual(
                review.get_rating(RatedModel.OVERALL_RATING),
                ReviewUtils.expected_overall[i]
            )

    def test_customer_interaction_rating(self):
        """Checks the customer interaction rating of a review works"""

        reviews = ReviewUtils.make_examples()

        for i, review in enumerate(reviews):
            self.assertEqual(
                review.get_rating(RatedModel.CUSTOMER_INTERACTION_RATING),
                ReviewUtils.rating_data[i]["customer_interaction_rating"]
            )

    def test_quality_rating(self):
        """Checks the customer interaction rating of a review works"""

        reviews = ReviewUtils.make_examples()

        for i, review in enumerate(reviews):
            self.assertEqual(
                review.get_rating(RatedModel.QUALITY_RATING),
                ReviewUtils.rating_data[i]["quality_rating"]
            )

    def test_price_rating(self):
        """Checks the customer interaction rating of a review works"""

        reviews = ReviewUtils.make_examples()

        for i, review in enumerate(reviews):
            self.assertEqual(
                review.get_rating(RatedModel.PRICE_RATING),
                ReviewUtils.rating_data[i]["price_rating"]
            )

class ShopUtils:
    """Helpers for ShopTest"""

    @staticmethod
    def make_example(n=1) -> Shop:
        """Makes an example Shop"""

        # Make base shop
        shop = Shop(
            name=f"Test shop {n}",
            description="Test description",
            # TODO: picture, categories, owners
            opening_hours="Test opening hours",
            location="TODO",
        )
        shop.save()

        # Add reviews to the shop
        ReviewUtils.make_examples(shop)

        return shop

class ShopTest(TestCase):
    """Tests for Shop"""

    def test_overall_stars(self):
        """Tests the overall star calculation of the example shop"""

        shop = ShopUtils.make_example()
        self.assertEqual(4, shop.get_stars(RatedModel.OVERALL_RATING))

    def test_customer_interaction_stars(self):
        """Tests the customer interaction star calculation of the example shop"""

        shop = ShopUtils.make_example()
        self.assertEqual(4, shop.get_stars(RatedModel.CUSTOMER_INTERACTION_RATING))

    def test_price_stars(self):
        """Tests the price star calculation of the example shop"""

        shop = ShopUtils.make_example()
        self.assertEqual(4, shop.get_stars(RatedModel.PRICE_RATING))


class ViewTestCase(TestCase):
    """Tests a view"""

    USERNAME = 'test'
    PASSWORD = 'test'

    client = Client()

    def login(self):
        user = User.objects.get_or_create(username='test')[0]
        user.set_password('test')
        user.save()
        self.client.login(username=self.USERNAME, password=self.PASSWORD)


class HomeViewTest(ViewTestCase):
    """Tests the home page view"""

    def test_navbar_logged_out(self):
        """Tests that the navbar shows Login and Sign Up when not logged in"""

        response = self.client.get(reverse('gsr:index'))
        self.assertContains(response, "Login")
        self.assertContains(response, "Signup")
        self.assertNotContains(response, "Logout")
        self.assertNotContains(response, "Profile")

    def test_navbar_logged_in(self):
        """Tests that the navbar shows Sign Out and Profile when not logged in"""

        self.login()
        response = self.client.get(reverse('gsr:index'))
        self.assertNotContains(response, "Login")
        self.assertNotContains(response, "Signup")
        self.assertContains(response, "Logout")
        self.assertContains(response, "Profile")

    def test_recently_added(self):
        """Tests that recently added is sorted by creation time"""

        # Create shops
        shops = []
        for i in range(5):
            shop = ShopUtils.make_example(i+1)
            shop.save()
            shops.append(shop)

        # Check shops are on page in reverse order
        response = self.client.get(reverse('gsr:index'))
        expected = [
            f"<Shop: {shop}>"
            for shop in reversed(shops)
        ]
        self.assertQuerysetEqual(response.context['shoplistbyadddate'], expected)

    def test_top_rated(self):
        """Tests that top rated is sorted by rating"""

        # Create shops with ascending ratings
        shops = []
        for i in range(5):
            shop = ShopUtils.make_example(i+1)
            shop.save()
            ReviewUtils.make_with_rating(shop, i)
            shops.append(shop)

        # Check shops are on page in reverse order
        response = self.client.get(reverse('gsr:index'))
        expected = to_query_set_strs(reversed(shops))
        self.assertQuerysetEqual(response.context['shoplistbystars'], expected)

    def test_recently_visited(self):
        """Tests that shops show up in recently visited when visited"""

        # Create shop
        shop = ShopUtils.make_example()
        shop.save()

        # Check shop not present before visiting
        response = self.client.get(reverse('gsr:index'))
        self.assertQuerysetEqual(response.context['shops_recently_visited'], [])

        # Visit shop
        self.client.get(reverse('gsr:view_shop', args=(shop.slug,)))

        # Check shop added
        response = self.client.get(reverse('gsr:index'))
        expected = to_query_set_strs([shop])
        self.assertQuerysetEqual(response.context['shops_recently_visited'], expected)
