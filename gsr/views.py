from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from gsr.models import Category, OwnerGroupRequest, RatedModel, Shop, Review, ReviewReply
from gsr.forms import CategoryForm, OwnerGroupRequestForm, ShopForm, UserForm, ReviewForm
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.http import JsonResponse

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
    return redirect(reverse('gsr:index'))

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
    shoplistbyadddate = Shop.objects.order_by('-date_added')
    shoplistbystars = [
        shop
        for shop in Shop.objects.all()
    ]
    shoplistbystars.sort(key=lambda s: -s.get_rating(RatedModel.OVERALL_RATING))

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

    SHOP_COUNT = 10
    context = {
        'shoplistbystars':shoplistbystars[:SHOP_COUNT],
        'shoplistbyadddate':shoplistbyadddate[:SHOP_COUNT],
        'shops_recently_visited':ordered_shops_recently_visited[:SHOP_COUNT],
    }

    return render(request, 'gsr/home.html', context)

@login_required
def user(request):
    thisUser = request.user
    shops = Shop.objects.filter(owners=thisUser)
    reviews = Review.objects.filter(author=thisUser)

    has_owner_group = thisUser.groups.filter(name="Shop Owner").exists()
    requested_owner_group = OwnerGroupRequest.objects.filter(user=thisUser).exists()

    return render(
        request,
        'gsr/user.html',
        {
            'user': thisUser,
            'reviews': reviews,
            'shops': shops,
            'has_owner_group': has_owner_group,
            'requested_owner_group': requested_owner_group,
        }
    )

def search(request: HttpRequest):
    # GET parameter names
    SEARCH_QUERY_PARAM = 'query'
    SEARCH_CATEGORY_PARAM = 'category'
    SEARCH_RATING_PARAM = 'rating'

    # Special category name for no filtering
    ANY_CATEGORY = 'Any'

    # GET parameter defaults
    default_category = ANY_CATEGORY
    default_rating_method = RatedModel.OVERALL_RATING

    # Get GET parameters from request url
    query = request.GET.get(SEARCH_QUERY_PARAM)
    rating_method = request.GET.get(SEARCH_RATING_PARAM, default_rating_method)
    category_name = request.GET.get(SEARCH_CATEGORY_PARAM, default_category)
    if category_name == ANY_CATEGORY:
        category_name = None
    
    category = None
    if category_name is not None:
        filtered = Category.objects.filter(name=category_name, is_approved=True)
        if filtered:
            category = filtered[0]

    # Filter shops by category and query, sort in descending order of rating
    results = [
        shop
        for shop in Shop.objects.all()
        if shop.matches_search(query, category_name)
    ]
    results.sort(key=lambda s: -s.get_rating(rating_method))

    # Build category name list for dropdown
    category_names = [ANY_CATEGORY] + [c.name for c in Category.objects.filter(is_approved=True)]

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

            # Category info header
            'category' : category,

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


@login_required
def create_reply(request,shop_name_slug):
    if request.method == 'POST':
        review_id = request.POST.get('review_id')
        comment = request.POST.get('comment')
        review = Review.objects.get(id=review_id)
        user = request.user
        reply = ReviewReply.objects.create(comment=comment, review=review,author=user)
        reply.save()
        return JsonResponse({'success': True,'username':user.username,'comment':comment})
    else:
        return JsonResponse({'success': False})
   
   


def edit_user(request: HttpRequest):
    # Check that user is logged in
    if not request.user.is_authenticated:
        return HttpResponse("You must be logged in to do that.", status=403)
    
    # Try change name if requested
    if 'name' in request.POST:
        request.user.username = request.POST['name']
        try:
            request.user.save()
        except IntegrityError:
            return HttpResponse("This username is taken.", status=406)
    
    # Try change email if requested
    if 'email' in request.POST:
        request.user.email = request.POST['email']
        try:
            request.user.save()
        except IntegrityError as e:
            return HttpResponse(e)

    return HttpResponse("Updated.")

def show_replies(request,shop_name_slug):
    reviewReplies = None
    if request.method == 'GET':
        review_id = request.GET.get('review_id')
        review = Review.objects.get(id=review_id)
        reviewReplies = ReviewReply.objects.filter(review=review)
        repliesList = []
        for reply in reviewReplies:
            repliesList.append([reply.author.username,reply.comment])

    return JsonResponse({'replies': repliesList})


def owner_request(request: HttpRequest):
    form = OwnerGroupRequestForm()
    if request.method == 'POST':
        form = OwnerGroupRequestForm(request.POST, request.FILES)
        if form.is_valid():
            req = form.save(commit=False)
            req.user = request.user
            req.save()
            return redirect(reverse('gsr:user'))
        else:
            print(form.errors)

    return render(request, 'gsr/owner_request.html', { 'form' : form })
