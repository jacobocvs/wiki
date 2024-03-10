from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path('search', views.search, name='search'),
    path('new_entry', views.new_entry, name='new_entry'),
    path('random', views.random_entry, name='random'),
    path('edit/<str:title>', views.edit, name='edit'),
]
