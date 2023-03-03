from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from gsr.forms import CategoryForm, ShopForm

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
