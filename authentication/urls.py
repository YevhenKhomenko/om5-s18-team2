
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='users'),
    path('users/<int:user_id>', detail, name='user'),
    path('create', create, name='create_user'),
    path('edit/<int:user_id>', edit, name='edit_user'),
    path('delete/<int:user_id>', delete_user, name='delete_user'),

    path('api/v1/user_list/', UserListAPIView.as_view() , name='user_list'),
    path('api/v1/<int:user_id>/', UserDetailAPIView.as_view() , name='user_detail_view'),
    path('api/v1/user_create/', UserCreateAPIView.as_view() , name='user_create'),


]