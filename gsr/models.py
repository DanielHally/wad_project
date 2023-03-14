from datetime import datetime
from typing import List

from django.contrib.auth.models import User
from django.db import models

# TODO: does anything need a UserProfile model? All attribtues in design's ERD are in django's User

# TODO: create shop owner user group


class DatedModel(models.Model):
    """A model with automatically handled date_added and date_updated attributes
    
    date_updated is set on save() based on any difference in the fields listed in DATED_FIELDS"""

    class Meta:
        abstract = True

    """The date the entity was created"""
    date_added = models.DateField(null=True)

    """The date the details of the entity were last changed"""
    date_updated = models.DateField(null=True)

    """The field names of the class to check for the dates of"""
    DATED_FIELDS = tuple()

    def has_updated(self, saved: models.Model) -> bool:
        """Checks whether the model has been updated compared to the saved version"""
        
        return any(
            getattr(self, fields) != getattr(saved, fields)
            for fields in self.DATED_FIELDS
        )

    def save(self, *args, **kwargs):
        """Override to handle date_added and date_updated"""

        # Get the current saved details
        prev = type(self).objects.filter(pk=self.pk).first()

        if prev is None:
            # Set date added & updated to now if just created
            self.date_added = datetime.now()
            self.date_updated = self.date_added
        elif self.has_updated(prev):
            # Set date updated to now if description fields changed
            self.date_updated = datetime.now()

        super().save(*args, **kwargs)


class Category(models.Model):
    """A category for shops
    
    These can be created by admins and requested by users in the shop owner group"""

    class Meta:
        verbose_name_plural = 'Categories'

    MAX_NAME_LENGTH = 32
    MAX_DESCRIPTION_LENGTH = 512

    """The display name of the category"""
    name = models.CharField(max_length=MAX_NAME_LENGTH)

    """The description of the category"""
    description = models.CharField(max_length=MAX_DESCRIPTION_LENGTH)

    """The icon for the category"""
    picture = models.ImageField(blank=True)

    def __str__(self) -> str:
        """Display a category by its name"""

        return self.name


class Shop(DatedModel):
    """A shop to be displayed on the website
    
    These can be created by users in the shop owner group"""

    # Constants
    MAX_NAME_LENGTH = 128
    MAX_DESCRIPTION_LENGTH = 8192
    MAX_OPENING_HOURS_LENGTH = 512
    MAX_LOCATION_LENGTH = 128

    """The display name of the shop"""
    name = models.CharField(max_length=MAX_NAME_LENGTH)

    """The owner's description of the shop"""
    description = models.CharField(max_length=MAX_DESCRIPTION_LENGTH, blank=True)

    """The icon picture for the shop"""
    picture = models.ImageField(upload_to='shop_images', blank=True)

    """The opening hours description of the shop"""
    opening_hours = models.CharField(max_length=MAX_OPENING_HOURS_LENGTH)

    """The location of the shop as a Google Maps Place Id string (q= parameter of embed url)"""
    location = models.CharField(max_length=MAX_LOCATION_LENGTH)

    """The categories this shop belongs to"""
    categories = models.ManyToManyField(Category)

    """The users who own this shop"""
    owners = models.ManyToManyField(User)

    """The number of times the shop's page has been viewed"""
    # TODO: should this be the number of users who viewed it instead?
    views = models.IntegerField(default=0)

    """Set the fields to trigger date_updated to change"""
    # TODO: categories views and owners?
    DATED_FIELDS = ('name', 'description', 'picture', 'opening_hours', 'location')

    def __str__(self) -> str:
        """Display a shop as its name"""

        return self.name

    def get_reviews(self) -> List["Review"]:
        """Gets all of the reviews for this shop"""

        return list(Review.objects.filter(shop=self))

    def _stars(self, rating_sum: float, count: int) -> int:
        if count == 0:
            return 0
        else:
            return round(rating_sum / count)

    def overall_rating(self) -> int:
        """Calculates the star rating for a shop"""

        reviews = self.get_reviews()
        return self._stars(sum(review.overall_rating() for review in reviews), len(reviews))
    
    def customer_interaction_rating(self) -> int:
        """Calculates the customer interaction star rating for a shop"""

        reviews = self.get_reviews()
        return self._stars(sum(review.customer_interaction_rating for review in reviews), len(reviews))

    def price_rating(self) -> int:
        """Calculates the price star rating for a shop"""

        reviews = self.get_reviews()
        return self._stars(sum(review.price_rating for review in reviews), len(reviews))

    def quality_rating(self) -> int:
        """Calculates the quality star rating for a shop"""

        reviews = self.get_reviews()
        return self._stars(sum(review.quality_rating for review in reviews), len(reviews))

    class RatingMethod:
        OVERALL_RATING = "Overall Rating"
        CUSTOMER_INTERACTION_RATING = "Customer Interaction Rating"
        QUALITY_RATING = "Quality Rating"
        PRICE_RATING = "Price Rating"

        methods = {
            OVERALL_RATING : lambda s: s.overall_rating(),
            CUSTOMER_INTERACTION_RATING : lambda s: s.customer_interaction_rating(),
            QUALITY_RATING : lambda s: s.quality_rating(),
            PRICE_RATING : lambda  s: s.price_rating(),
        }


class Review(DatedModel):
    """A review of a shop
    
    These can be created by any user on any shop"""

    STAR_CHOICES = [(x, f"{x} stars") for x in range(1, 6)]
    MAX_COMMENT_LENGTH = 512

    """The shop being reviewed"""
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    """The user who wrote the review"""
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    """The stars given for the customer interaction of the shop"""
    customer_interaction_rating = models.IntegerField(choices=STAR_CHOICES)

    """The stars given for the price of products at the shop"""
    price_rating = models.IntegerField(choices=STAR_CHOICES)

    """The stars given for the quality of products at the shop"""
    quality_rating = models.IntegerField(choices=STAR_CHOICES)

    """The comment left by the reviewer"""
    comment = models.CharField(max_length=MAX_COMMENT_LENGTH, blank=True)

    """Set the fields to trigger date_updated to change"""
    DATED_FIELDS = ('customer_interaction_rating', 'price_rating', 'quality_rating', 'comment')

    def __str__(self) -> str:
        """Display a review by its stars and the start of its comment"""

        stars = (self.customer_interaction_rating, self.price_rating, self.quality_rating)
        return f"Review({stars} \"{self.comment[:10]}...\")"

    def overall_rating(self) -> float:
        """Calculates the overall star rating for a review"""

        return (self.customer_interaction_rating + self.price_rating + self.quality_rating) / 3


class ReviewReply(DatedModel):
    """A reply to a review of a shop
    
    These can be created by any user on any review"""

    class Meta:
        verbose_name_plural = 'Review replies'

    """The review being replied to"""
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    """The user who wrote the reply"""
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    """The text of the reply"""
    comment = models.CharField(max_length=Review.MAX_COMMENT_LENGTH)

    def __str__(self) -> str:
        """Display a reply by its comment and the string for its target review"""

        return f"ReviewReply(\"{self.comment[:10]}...\", {self.review})"
