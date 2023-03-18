from io import BytesIO
from django import forms
from django.contrib.auth.models import User
from PIL import Image

from gsr.models import Category, Shop, Review, ReviewReply


class CategoryForm(forms.ModelForm):
    """A form to create a new category
    
    TODO: this needs admin approval in some way"""

    class Meta:
        model = Category
        fields = ('name', 'description')


class ShopForm(forms.ModelForm):
    """A form to create a new shop"""
    
    # Override to only select users in owner group
    # owners = forms.ModelMultipleChoiceField(User.objects.filter(groups__name='Shop Owner'))

    def clean(self):
        # Resize picture to square
        picture = self.cleaned_data.get('picture')
        if picture is not None:
            image = Image.open(BytesIO(picture.read()))
            image = image.resize((256, 256), Image.ANTIALIAS)
            new_image = BytesIO()
            image.save(new_image, 'PNG')
            picture.file = new_image

        return self.cleaned_data

    
    class Meta:
        model = Shop
        fields = ('name', 'description', 'picture', 'opening_hours', 'location', 'categories')
        
        widgets = {
            "picture" : forms.FileInput(attrs={
                "id" : "image_field",
                "class" : "gsr-cream",
                }),
            "categories" : forms.CheckboxSelectMultiple(attrs={
                "id" : "categories",
                "class" : "list-unstyled",
                
                }),
            "description" : forms.Textarea(attrs={
                'rows': '5',
                'cols': '100', 
                'class':'gsr-cream', 
                'style':'resize:none;width:90%;', 
                }),
            "name" : forms.TextInput(attrs={
                "class" : "gsr-cream"
                }),
            "location" : forms.Textarea(attrs={
                'rows': '4',
                'cols': '100', 
                'class':'gsr-cream', 
                'style':'resize:none;width:90%;', 
                }),
            "opening_hours" : forms.Textarea(attrs={
                'rows': '4',
                'cols': '100', 
                'class':'gsr-cream', 
                'style':'resize:none;width:90%;', 
                }),
                
        }



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','email','password','groups')
        
        widgets = {
            "groups" : forms.CheckboxSelectMultiple(attrs={
                    "id" : "categories",
                    "class" : " list-unstyled",
                    
                    }),
                    
                }
