from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='authors'),
    path('/<int:author_id>', detail, name='author'),
    path('/add_author', add_author, name='add_author'),
    path('add_author/<int:author_id>', add_author, name='add_author'),
    path('delete/<int:author_id>', del_author, name='del_author'),

    path('api/v1/author_list', AuthorListAPIView.as_view(), name='author_list_view'),
    path('api/v1/<int:author_id>/', AuthorDetailAPIView.as_view(), name='author_detail_view'),
    path('api/v1/author_create/', AuthorCreateAPIView.as_view(), name='author_create_view'),

]
