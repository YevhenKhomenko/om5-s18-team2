from . import views
from django.urls import path


urlpatterns = [
    path('', views.first_view, name='orders'),
    path('bad_users/', views.bad_users),
    path('<int:order_id>/', views.order_details, name='order_details'),
    path('create_order/', views.create_order, name='create_order'),
    path('delete_order/<int:order_id>', views.delete_order, name='delete_order'),

    path('api/v1/order_list/', views.OrderListView.as_view(), name='api_order_list'),
    path('api/v1/<int:order_id>/', views.OrderDetailsView.as_view(), name='api_order_details'),
    path('api/v1/create_order/', views.CreateOrderView.as_view(), name='api_create_order')

]

