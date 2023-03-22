from django.urls import path

from gsr import views

app_name = 'gsr'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/',views.user_signup,name = 'signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add_shop/', views.add_shop, name='add_shop'),
    path('add_category/', views.add_category, name='add_category'),
    path('user/',views.user, name = 'user'),
    path('search/', views.search, name='search'),
    path('shop/<slug:shop_name_slug>/',views.view_shop,name ='view_shop'),
    path('delete_account/', views.delete_account , name='delete_account'),
    path('shop/<slug:shop_name_slug>/edit_shop',views.edit_shop,name ='edit_shop'),
    path('shop/<slug:shop_name_slug>/add_review',views.add_review,name='add_review'),
    path('shop/<slug:shop_name_slug>/create_reply/', views.create_reply, name='create_reply'),
    path('shop/<slug:shop_name_slug>/show_replies/',views.show_replies,name='show_replies'),
    path('edit_user/', views.edit_user, name='edit_user'),


]
