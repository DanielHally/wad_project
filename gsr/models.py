from abc import abstractmethod
from typing import List, Optional

from django.contrib.auth.models import Group, User
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.urls import reverse



class RatedModel:
    OVERALL_RATING = "Overall Rating"
    CUSTOMER_INTERACTION_RATING = "Customer Interaction Rating"
    QUALITY_RATING = "Quality Rating"
    PRICE_RATING = "Price Rating"

    METHODS = [
        OVERALL_RATING,
        CUSTOMER_INTERACTION_RATING,
        QUALITY_RATING,
        PRICE_RATING,
    ]
    
    def get_stars(self, method: str = OVERALL_RATING) -> int:
        """Gets the star rating for a specific method"""

        return round(self.get_rating(method))
    
    @abstractmethod
    def get_rating(self, method: str = OVERALL_RATING) -> float:
        """Gets the rating for a specific method"""

        raise NotImplementedError


class DatedModel(models.Model):
    """A model with automatically handled date_added and date_updated attributes
    
    date_updated is set on save() based on any difference in the fields listed in DATED_FIELDS"""

    class Meta:
        abstract = True

    """The date the entity was created"""
    date_added = models.DateTimeField(null=True)

    """The date the details of the entity were last changed"""
    date_updated = models.DateTimeField(null=True)

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
            self.date_added = timezone.now()
            self.date_updated = self.date_added
        elif self.has_updated(prev):
            # Set date updated to now if description fields changed
            self.date_updated = timezone.now()

        super().save(*args, **kwargs)


class Category(models.Model):
    """A category for shops
    
    These can be created by admins and requested by users in the shop owner group"""

    class Meta:
        verbose_name_plural = 'Categories'

    MAX_NAME_LENGTH = 32
    MAX_DESCRIPTION_LENGTH = 512

    MEDIA_SUBDIR = 'category_images'

    DEFAULT_PICTURE = static('category_default_picture.png')

    """The display name of the category"""
    name = models.CharField(max_length=MAX_NAME_LENGTH)

    """The description of the category"""
    description = models.TextField(max_length=MAX_DESCRIPTION_LENGTH)

    """The icon for the category"""
    picture = models.ImageField(upload_to=MEDIA_SUBDIR, blank=True)
    
    """True/False, states whether category is approved or not"""
    is_approved = models.BooleanField(default=False)

    def __str__(self) -> str:
        """Display a category by its name"""

        return self.name


class Shop(DatedModel, RatedModel):
    """A shop to be displayed on the website
    
    These can be created by users in the shop owner group"""

    # Constants
    MAX_NAME_LENGTH = 128
    MAX_DESCRIPTION_LENGTH = 8192
    MAX_OPENING_HOURS_LENGTH = 512
    MAX_LOCATION_LENGTH = 128

    DEFAULT_PICTURE = static('shop_default_picture.png')

    MEDIA_SUBDIR = 'shop_images'


    """The display name of the shop"""
    name = models.CharField(max_length=MAX_NAME_LENGTH)

    """The name of the shop in links"""
    slug = models.SlugField(unique=True)

    """The owner's description of the shop"""
    description = models.TextField(max_length=MAX_DESCRIPTION_LENGTH, blank=True)

    """The icon picture for the shop"""
    picture = models.ImageField(upload_to=MEDIA_SUBDIR, blank=True)

    """The opening hours description of the shop"""
    opening_hours = models.TextField(max_length=MAX_OPENING_HOURS_LENGTH)

    """The location of the shop as a Google Maps Place Id string (q= parameter of embed url)"""
    location = models.TextField(max_length=MAX_LOCATION_LENGTH)

    """The categories this shop belongs to"""
    categories = models.ManyToManyField(Category)

    """The users who own this shop"""
    owners = models.ManyToManyField(User)

    """Set the fields to trigger date_updated to change"""
    DATED_FIELDS = ('name', 'description', 'picture', 'opening_hours', 'location')

    class Meta:
        permissions = [
            ("manage_shops", "Can create and edit shops"),
        ]

    def __str__(self) -> str:
        """Display a shop as its name"""

        return self.name

    def get_reviews(self) -> List["Review"]:
        """Gets all of the reviews for this shop"""

        return list(Review.objects.filter(shop=self))

    def matches_search(self, query: Optional[str], category_name: Optional[str]) -> bool:
        """Checks if a Shop should be included in a search result"""

        accept = True

        # Check category
        if category_name is not None:
            if not self.categories.filter(name=category_name).exists():
                accept = False
        
        # Check query in name and description
        if query is not None:
            query = query.lower()
            if query not in self.name.lower() and query not in self.description.lower():
                accept = False
        
        return accept
    
    def get_rating(self, method: str = RatedModel.OVERALL_RATING) -> float:
        """Gets the average rating of reviews for a specific method"""

        reviews = self.get_reviews()
        if len(reviews) == 0:
            return 0
        else:
            total = 0
            for review in self.get_reviews():
                total += review.get_rating(method)

            return total / len(reviews)
        
    def get_owners(self):
        return self.owners.all()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Shop, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('gsr:view_shop', kwargs={'shop_name_slug': self.slug})
    
    def get_edit_url(self):
        return reverse('gsr:edit_shop', kwargs={'shop_name_slug': self.slug})

class Review(DatedModel, RatedModel):
    """A review of a shop
    
    These can be created by any user on any shop"""

    STARS_MIN = 1
    STARS_MAX = 5
    STAR_CHOICES = [(x, f"{x} stars") for x in range(STARS_MIN, STARS_MAX+1)]
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
    comment = models.TextField(max_length=MAX_COMMENT_LENGTH, blank=True)

    """Set the fields to trigger date_updated to change"""
    DATED_FIELDS = ('customer_interaction_rating', 'price_rating', 'quality_rating', 'comment')

    def __str__(self) -> str:
        """Display a review by its stars and the start of its comment"""

        stars = (self.customer_interaction_rating, self.price_rating, self.quality_rating)
        return f"Review({stars} \"{self.comment[:10]}...\")"

    def overall_rating(self) -> float:
        """Calculates the overall star rating for a review"""

        return (self.customer_interaction_rating + self.price_rating + self.quality_rating) / 3

    def get_rating(self, method: str = RatedModel.OVERALL_RATING) -> float:
        """Gets therating of this review for a specific method"""

        if method == RatedModel.CUSTOMER_INTERACTION_RATING:
            return float(self.customer_interaction_rating)
        elif method == RatedModel.PRICE_RATING:
            return float(self.price_rating)
        elif method == RatedModel.QUALITY_RATING:
            return float(self.quality_rating)
        else:
            return self.overall_rating()
        
    def get_author(self):
        return self.author


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
    comment = models.TextField(max_length=Review.MAX_COMMENT_LENGTH)

    def __str__(self) -> str:
        """Display a reply by its comment and the string for its target review"""

        return f"ReviewReply(\"{self.comment[:10]}...\", {self.review})"

class OwnerGroupRequest(DatedModel):
    """A request for a user to be in hte shop owner group"""

    MAX_COMMENT_LENGTH = 2048
    MEDIA_SUBDIR = 'owner_evidence'

    """The user requesting the owner role"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    """The user's description of why they should be admin"""
    request_comment = models.TextField(blank=False, max_length=MAX_COMMENT_LENGTH)

    """A file included by the user"""
    evidence_file = models.FileField(upload_to=MEDIA_SUBDIR)

    """Whether the request has been approved by an admin
    
    Triggers the group promotion and deletion of the request on save"""
    approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """Override to apply the application if approved"""
        super().save(*args, **kwargs)

        if self.approved:
            print(f"Promoting user {self.user.username} to Shop Owner Group")
            group = Group.objects.get(name="Shop Owner")
            self.user.groups.add(group)
            self.user.save()
            self.delete()
    
    def __str__(self):
        """Include username in print"""

        return f"OwnerGroupRequest({self.user.username})"
