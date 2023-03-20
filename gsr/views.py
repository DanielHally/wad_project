from itertools import chain
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from gsr.models import Category, RatedModel, Shop, Review
from gsr.forms import CategoryForm, ShopForm, UserForm


# Create your views here.
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
                dest = request.POST.get('next')
                if dest is None or dest == "":
                    dest = reverse('gsr:index')
                return redirect(dest)
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
def delete_account(request):
    user = request.user
    user.delete()
    logout(request)
    return redirect('home')

@login_required
def add_shop(request):
    form = ShopForm()

    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES)
        
        
        if form.is_valid():
            shop = form.save(commit=True)
            shop.owners.set([request.user])
            shop.save()
            return redirect('/gsr/')
        else:
            print(form.errors)

    return render(request, 'gsr/add_shop.html', {'form': form})

def view_shop(request,shop_name_slug):
    context_dict = {}
    try:
        shop = Shop.objects.get(slug=shop_name_slug)
        reviews = Review.objects.filter(shop=shop)
        categories = [category.name for category in shop.categories.all()]

        """changes splits by new line to make the template take a new line"""
        shop.opening_hours = shop.opening_hours.split("\n")
        context_dict['shop'] = shop
        context_dict['reviews'] = reviews
        context_dict['categories'] = categories

    except Shop.DoesNotExist:
        context_dict['shop'] = None
        context_dict['reviews'] = None
        context_dict['categories'] = None


    return render(request,'gsr/view_shop.html',context = context_dict)



def index(request):
    QUERY_PARAM = 'query'
    CATEGORY_PARAM = 'category'
    RATING_PARAM = 'rating'

    # Special category name for no filtering
    ANY_CATEGORY = 'Any'

    # GET parameter defaults
    default_category = ANY_CATEGORY
    default_rating_method = RatedModel.OVERALL_RATING

    # Get GET parameters from request url
    query = request.GET.get(QUERY_PARAM)
    rating_method = request.GET.get(RATING_PARAM, default_rating_method)
    category = request.GET.get(CATEGORY_PARAM, default_category)
    if category == ANY_CATEGORY:
        category = None

    shoplistbyadddate = Shop.objects.order_by('-date_added')[:5]
    shoplistbystars = [
        shop
        for shop in Shop.objects.all()
        if shop.matches_search(query, category)
    ]
    shoplistbystars.sort(key=lambda s: -s.get_rating(rating_method))

    shoplistbystars_names = [
        shop.name
        for shop in shoplistbystars
    ]
    
    shoplistbyadddate_names=[
        shop.name
        for shop in shoplistbyadddate
    ]
    shoplistbystars_stars = [
        shop.get_stars(RatedModel.OVERALL_RATING)
        for shop in shoplistbystars
    ]

    shoplistbyadddate_stars = [
        shop.get_stars(RatedModel.OVERALL_RATING)
        for shop in shoplistbyadddate
    ]
    shoplistbystars_name1= shoplistbystars_names[0]
    shoplistbystars_stars1 = [i for i in range(shoplistbystars_stars[0])]
    shoplistbystars_stars2 = [i for i in range(shoplistbystars_stars[1])]
    ##shoplistbystars_stars3 = [i for i in range(shoplistbystars_stars[2])]
   ## shoplistbystars_stars4 = [i for i in range(shoplistbystars_stars[3])]
   ## shoplistbystars_stars5 = [i for i in range(shoplistbystars_stars[4])]
    shoplistbystars_grey1 = [i for i in range(5-shoplistbystars_stars[0])]
    shoplistbystars_grey2 = [i for i in range(5 - shoplistbystars_stars[1])]

    context = {'shoplistbyadddate_stars': shoplistbyadddate_stars,'shoplistbyadddate_names':shoplistbyadddate_names,
               'shoplistbystars_stars':shoplistbystars_stars,'shoplistbystars_names':shoplistbystars_names,
               'shoplistbystars_stars1':shoplistbystars_stars1,'shoplistbystars_stars2':shoplistbystars_stars2,
               'shoplistbystars_grey1':shoplistbystars_grey1,'shoplistbystars_grey2':shoplistbystars_grey2,
               'shoplistbystars_name1':shoplistbystars_name1,'shoplistbystars':shoplistbystars,'shoplistbyadddate':shoplistbyadddate
               }

    return render(request, 'gsr/home.html', context)

@login_required
def user(request):
    thisUser = request.user
    shops = []
    for shop in Shop.objects.all():
        for owner in shop.get_owners():
            print(thisUser.username, owner)
            if str(thisUser.username) == str(owner):
                shops.append(shop)
    print(shops)
    reviews = []
    for review in Review.objects.all():
        if str(thisUser.username) == str(review.get_author()):
            reviews.append(review)

    
    return render(request, 'gsr/user.html', {'user': thisUser,'reviews':reviews})

def search(request: HttpRequest):
    # GET parameter names
    QUERY_PARAM = 'query'
    CATEGORY_PARAM = 'category'
    RATING_PARAM = 'rating'

    # Special category name for no filtering
    ANY_CATEGORY = 'Any'

    # GET parameter defaults
    default_category = ANY_CATEGORY
    default_rating_method = RatedModel.OVERALL_RATING

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
    results.sort(key=lambda s: -s.get_rating(rating_method))

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
            'rating_methods' : RatedModel.METHODS,
            'default_rating_method' : default_rating_method,

            # Results generation
            'rating_method' : rating_method,
            'results' : results,
        }
    )
