from . import views
from django.urls import path


urlpatterns = [
    path('', views.first_view, name='books'),
    path('author/', views.by_author),
    path('user/', views.by_user),
    path('detail/', views.detail),
    path('detail/<received_id>', views.detail),
    path('unordered/', views.unordered),
    path('add_book/', views.add_book, name='add_book'),
    path('delete_book/<int:book_id>', views.delete_book, name='delete_book'),
]

