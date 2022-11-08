from django.urls import path
from home.customer import views
from home import views as home_views

urlpatterns = [
    path('', views.customer, name='customer'),
    path('order/<int:id>/', views.order_detail, name='customer-order-detail'),
    path('review/<int:id>/', views.review, name='customer-kutish'),
    path('my-orders/', views.myorders, name='customer-my-orders'),
    path('delete-order/<int:id>/', views.delete_order, name='delete-order'),
    path('right-order/<int:id>/', views.right_order, name='right-order'),
    path('black-list/<int:id>/', views.black_list, name='black-list'),

    path('customer-order-update/<int:id>/', views.customer_order_update, name='customer-order-update')
]
