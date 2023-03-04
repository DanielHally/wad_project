from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

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

def user_signup(request):
    """TODO: Need to change the groups input probably to a boolean of is shop owner
    or not shop owner"""
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

    return render(request,'gsr/signup.html',context={'user_form':user_form,'registered':registered})


def user_login(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:

                login(request, user)
                return redirect(reverse('gsr:index'))
            else:
                return render(request, 'gsr/login.html', context={"error": "Your account is disabled"})
        else:
            return render(request, 'gsr/login.html', context={"error": "Invalid login details"})
    else:
        return render(request, 'gsr/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('gsr:index'))

