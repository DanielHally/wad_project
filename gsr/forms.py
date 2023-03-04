from django import forms
from django.contrib.auth.models import User

from gsr.models import Category, Shop, Review, ReviewReply


class CategoryForm(forms.ModelForm):
    """A form to create a new category
    
    TODO: this needs admin approval in some way"""

    # Override to enforce max lengths
    name = forms.CharField(max_length=Category.MAX_NAME_LENGTH)
    description = forms.CharField(max_length=Category.MAX_DESCRIPTION_LENGTH)

    class Meta:
        model = Category
        fields = ('name', 'description')


class ShopForm(forms.ModelForm):
    """A form to create a new shop"""

    # Override to enforce max lengths
    name = forms.CharField(max_length=Shop.MAX_NAME_LENGTH)
    description = forms.CharField(max_length=Shop.MAX_DESCRIPTION_LENGTH)
    opening_hours = forms.CharField(max_length=Shop.MAX_OPENING_HOURS_LENGTH)
    location = forms.CharField(label="Google Maps Location Code", max_length=Shop.MAX_LOCATION_LENGTH)
    
    # Override to only select users in owner group
    owners = forms.ModelMultipleChoiceField(User.objects.filter(groups__name='Shop Owner'))

    class Meta:
        model = Shop
        fields = ('name', 'description', 'picture', 'opening_hours', 'location', 'categories', 'owners')



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','email','password','groups')