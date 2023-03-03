from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from gsr.forms import CategoryForm, ShopForm, UserForm


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'gsr/index.html')


def test_category_form(request: HttpRequest) -> HttpResponse:
    """A page to test CategoryForm, not for use in final site"""

    success = False
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
        else:
            print(form.errors)
    else:
        form = CategoryForm()

    return render(request, 'gsr/test/categoryform.html', context={'form': form, 'success': success})


def test_shop_form(request: HttpRequest) -> HttpResponse:
    """A page to test ShopForm, not for use in final site"""

    success = False
    if request.method == 'POST':
        form = ShopForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
        else:
            print(form.errors)
    else:
        form = ShopForm()

    return render(request, 'gsr/test/shopform.html', context={'form': form, 'success': success})

def signup(request):
    """TODO: Need to change the groups input probably to a boolean of is shop owner
    or not shop owner also change url as it kind of poopy"""
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user=user_form.save()

            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(request,'gsr/sign_up.html',context={'user_form':user_form,'registered':registered})


