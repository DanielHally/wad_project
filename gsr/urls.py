from django.urls import path

from gsr import views

app_name = 'gsr'

urlpatterns = [
    path('', views.index, name='index'),
    path('test/categoryform/', views.test_category_form, name='test_category_form')
]
