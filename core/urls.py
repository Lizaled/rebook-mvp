from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookListView.as_view(), name='catalog'),
    path('register/', views.register_view, name='register'),
    path('add-book/', views.BookCreateView.as_view(), name='add_book'),
    path('profile/', views.profile_view, name='profile'),
]