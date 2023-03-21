from itertools import chain
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from gsr.models import Category, RatedModel, Shop, Review
from gsr.forms import CategoryForm, ShopForm, UserForm, ReviewForm
from django.contrib.staticfiles.templatetags.staticfiles import static

# Create your views here.

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
    
    if request.method == 'GET':
        reason = request.GET.get("reason")
        messages = {"No_Role_On_Add" : "You can't add a shop without an owner account",
                    "No_Role_On_Edit": "You can't edit a shop without an owner account",
                    "Unowned_Shop"   : "You can't edit a shop you don't own"}
        error = messages.get(reason, "")        
    elif request.method == 'POST':

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
    
    return render(request, 'gsr/login.html', context={"error" : error})


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
    if not request.user.has_perm('gsr.manage_shops'):
        return redirect(reverse("gsr:login")+"?reason=No_Role_On_Add")
    
    form = ShopForm()
    context_dict = {}
    
    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES)
        
        
        if form.is_valid():
            shop = form.save(commit=True)
            shop.owners.set([request.user])
            shop.save()
            return redirect('/gsr/')
        else:
            print(form.errors)
    
    context_dict['picture'] = Shop.DEFAULT_PICTURE
    context_dict['form'] = form
    context_dict['action'] = reverse("gsr:add_shop")
    context_dict['title'] = "Add Your Shop"
    context_dict['submit_text'] = "Create Shop"
    
    return render(request, 'gsr/add_shop.html', context = context_dict)


@login_required
def add_category(request):
    if not request.user.has_perm('gsr.manage_shops'):
        return redirect(reverse("gsr:login")+"?reason=No_Role_On_Add")
    
    form = CategoryForm()
    context_dict = {}
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        
        
        if form.is_valid():
            category = form.save(commit=True)
            return redirect('/gsr/')
        else:
            print(form.errors)
    
    context_dict['form'] = form
    context_dict['action'] = reverse("gsr:add_category")
    context_dict['title'] = "Request a new Category"
    context_dict['submit_text'] = "Send for approval"
    
    return render(request, 'gsr/add_category.html', context = context_dict)

def update_recently_visited(request: HttpRequest, response: HttpResponse, shop: Shop):
    """Updates the user's recently visited shop list"""

    # Read cookie
    raw = request.COOKIES.get('recently_visited')
    if raw is not None and len(raw) > 0:
        names = raw.split(':')
    else:
        names = []

    # Update recently visited
    if shop.slug in names:
        names.remove(shop.slug)
    names.insert(0, shop.slug)
    names = names[:10]

    # Write cookie
    response.set_cookie('recently_visited', ':'.join(names))


def view_shop(request,shop_name_slug):
    context_dict = {}
    try:
        shop = Shop.objects.get(slug=shop_name_slug)
        reviews = Review.objects.filter(shop=shop)
        categories = [category.name for category in shop.categories.all()]

        """splits by new line to make the template take a new line"""
        shop.opening_hours = shop.opening_hours.split("\n")

        context_dict['shop'] = shop
        context_dict['reviews'] = reviews
        context_dict['categories'] = categories

    except Shop.DoesNotExist:
        shop = None
        context_dict['shop'] = None
        context_dict['reviews'] = None
        context_dict['categories'] = None


    response = render(request,'gsr/view_shop.html',context = context_dict)
    
    if shop is not None:
        update_recently_visited(request, response, shop)
    
    return response

@login_required
def edit_shop(request,shop_name_slug):
    if not request.user.has_perm('gsr.manage_shops'):
        return redirect(reverse("gsr:login")+"?reason=No_Role_On_Edit")
    
    context_dict = {}
    context_dict['picture'] = Shop.DEFAULT_PICTURE
    shop = get_object_or_404(Shop, slug=shop_name_slug)
    
    if request.user not in shop.owners.all() and not request.user.is_superuser: 
        return redirect(reverse("gsr:login")+"?reason=Unowned_Shop")
    
    categories = [category.name for category in shop.categories.all()]
    
    context_dict['shop'] = shop
    context_dict['categories'] = categories
    if shop.picture:
        context_dict['picture'] = shop.picture.url
        
    
    form = ShopForm(instance=shop)

    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES, instance=shop)
        
        if form.is_valid():
            shop = form.save(commit=True)
            return redirect(reverse("gsr:view_shop", args=[shop.slug] ))
        else:
            print(form.errors)
    
    context_dict['form'] = form
    context_dict['action'] = reverse("gsr:edit_shop", args=[shop.slug])
    context_dict['title'] = "Edit \"" + shop.name + "\""
    context_dict['submit_text'] = "Save Changes"
    
    return render(request,'gsr/add_shop.html', context = context_dict)


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

    ##raw cookies
    raw = request.COOKIES.get('recently_visited')
    if raw is not None and len(raw) > 0:
        names = raw.split(':')
    else:
        names = []
    # Query the database to get the Shop objects based on the slugs in the 'names' list
    shops_queryset = Shop.objects.filter(slug__in=names)

    # Create a dictionary with the slugs as keys and the Shop objects as values
    slug_to_shop = {shop.slug: shop for shop in shops_queryset}

    # Iterate through the 'names' list and create a new list of Shop objects
    ordered_shops_recently_visited = [slug_to_shop[slug] for slug in names if slug in slug_to_shop]

    context = {'shoplistbyadddate_stars': shoplistbyadddate_stars,'shoplistbyadddate_names':shoplistbyadddate_names,
               'shoplistbystars_stars':shoplistbystars_stars,'shoplistbystars_names':shoplistbystars_names,
               'shoplistbystars':shoplistbystars,'shoplistbyadddate':shoplistbyadddate,'shops_recently_visited':ordered_shops_recently_visited
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

@login_required
def add_review(request,shop_name_slug):
    try:
        shop = Shop.objects.get(slug=shop_name_slug)
    except Shop.DoesNotExist:
        shop = None

    if shop is None:
        return redirect('/gsr/')

    form = ReviewForm()

    if request.method =='POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.shop = shop
            review.author = request.user
            review.save()
            return redirect(reverse('gsr:view_shop',kwargs={'shop_name_slug':shop_name_slug}))

    context_dict = {'form':form,'shop':shop}
    return render(request, 'gsr/add_review.html', context= context_dict)
   
   
