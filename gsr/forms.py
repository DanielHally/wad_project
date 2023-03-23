from io import BytesIO
from django import forms
from django.contrib.auth.models import User
from PIL import Image

from gsr.models import Category, OwnerGroupRequest, Shop, Review, ReviewReply


class CategoryForm(forms.ModelForm):
    """A form to create a new category"""

    class Meta:
        model = Category
        fields = ('name', 'description', 'picture')
        widgets = {
            "name" : forms.TextInput(attrs={
                "class" : "gsr-cream"
                }),
            "description" : forms.Textarea(attrs={
                'rows': '5',
                'cols': '100', 
                'class':'gsr-cream', 
                'style':'resize:none;width:90%;', 
                }),
        }


class ShopForm(forms.ModelForm):
    """A form to create a new shop"""
    
    # Override to only select users in owner group
    # owners = forms.ModelMultipleChoiceField(User.objects.filter(groups__name='Shop Owner'))
    
    def clean(self):
        # Resize picture to square
        picture = self.cleaned_data.get('picture')
        if picture:
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
            "picture" : forms.ClearableFileInput(attrs={
                "id" : "image_field",
                "class" : "gsr-cream  border gsr-border",
                'style':'width:90%;',
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
            "location" : forms.HiddenInput(attrs={
                'id' : 'location',
                }),
            "opening_hours" : forms.Textarea(attrs={
                'rows': '5',
                'cols': '100', 
                'class':'gsr-cream', 
                'style':'resize:none;width:90%;', 
                }),
                
        }
        
    def __init__(self,*args,**kwargs):
        super (ShopForm,self ).__init__(*args,**kwargs)
        self.fields['categories'].queryset = Category.objects.filter(is_approved=True)



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


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('customer_interaction_rating','price_rating','quality_rating','comment')

        widgets = {
            "comment": forms.Textarea(attrs={
                "style":'height:300px;',
            })
        }


class OwnerGroupRequestForm(forms.ModelForm):
    class Meta:
        model = OwnerGroupRequest
        fields = ('request_comment', 'evidence_file')
        help_texts = {
            'request_comment' : "Please describe why you would like the shop owner permissions.",
            'evidence_file' : "Please upload some evidence, such as a photo or pdf with more information.",
        }
