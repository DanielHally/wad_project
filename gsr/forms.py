from django import forms
from django.contrib.auth.models import User

from gsr.models import Category, Shop, Review, ReviewReply


class CategoryForm(forms.ModelForm):
    """A form to create a new category
    
    TODO: this needs admin approval in some way"""

    name = forms.CharField(max_length=Category.MAX_NAME_LENGTH)
    description = forms.CharField(max_length=Category.MAX_DESCRIPTION_LENGTH)

    class Meta:
        model = Category
        fields = ('name', 'description')
