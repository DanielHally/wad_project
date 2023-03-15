from itertools import chain
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from gsr.models import Category, Shop
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
            user = user_form.save()

            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(request, 'gsr/signup.html', context={'user_form': user_form, 'registered': registered})


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


@login_required
def add_shop(request):
    form = ShopForm()

    if request.method == 'POST':
        form = ShopForm(request.POST)

        if form.is_valid():
            # form.save(commit=True)

            return redirect('/gsr/')
        else:
            print(form.errors)

    return render(request, 'gsr/add_shop.html', {'form': form})


def home(request):
    data = Shop.overall_rating()
    starsyellow = []
    for i in range(data):
        starsyellow.append(1)
    starsgery = []
    for i in range(5-data):
        starsgery.append(1)
   
    context = {'starsyellow': starsyellow, 'starsgery': starsgery,'shopname': shop.name}
    return render(request, 'home.html', context)

def user(request):
    return render(request, 'user.html')

def search(request: HttpRequest):
    # GET parameter names
    QUERY_PARAM = 'query'
    CATEGORY_PARAM = 'category'
    RATING_PARAM = 'rating'

    # Special category name for no filtering
    ANY_CATEGORY = 'Any'

    # GET parameter defaults
    default_category = ANY_CATEGORY
    default_rating_method = Shop.RatingMethod.OVERALL_RATING

    # Get GET parameters from request url
    query = request.GET.get(QUERY_PARAM)
    rating_method = request.GET.get(RATING_PARAM, default_rating_method)
    category = request.GET.get(CATEGORY_PARAM, default_category)
    if category == ANY_CATEGORY:
        category = None

    # Filter shops by category and query, sort in descending order of rating
    results = [
        shop
        for shop in Shop.objects.all()
        if shop.matches_search(query, category)
    ]
    results.sort(key=lambda s: -Shop.RatingMethod.methods[rating_method](s))

    # Build category name list for dropdown
    category_names = [ANY_CATEGORY] + [c.name for c in Category.objects.all()]

    # Return rendered template
    return render(
        request,
        'gsr/search.html',
        {
            # Form filling
            'category_names' : category_names,
            'default_category' : default_category,
            'rating_methods' : Shop.RatingMethod.methods.keys(),
            'default_rating_method' : default_rating_method,

            # Results generation
            'rating_method' : rating_method,
            'results' : results,
        }
    )
