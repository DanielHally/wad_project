from django.urls import path

from gsr import views

app_name = 'gsr'

urlpatterns = [
    path('', views.index, name='index'),
    path('test/categoryform/', views.test_category_form, name='test_category_form'),
    path('test/shopform/', views.test_shop_form, name='test_shop_form'),
    path('signup/',views.user_signup,name = 'signup'),
    path('login/', views.user_login, name='login')
]