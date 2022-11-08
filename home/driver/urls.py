from django.urls import path
from home.driver import views

urlpatterns = [
    path('', views.driver_home, name='driver-home'),
    path('orders/', views.index, name='driver'),
    path('order/<int:id>/', views.order_detail, name='driver-order-detail'),
    path('accept-order/<int:id>/', views.accept_order, name='driver-accept-order'),

    path('kutish/', views.kutish, name='driver-kutish'),
    path('my-orders/', views.myorders, name='driver-myorders'),

    path('about-order/<int:id>/', views.about_order, name='driver-about-order'),

    path('close-order/<int:id>/', views.close_order, name='driver-close-order'),
    path('client-in-car/<int:id>/', views.client_in_car, name='driver-client-in-car'),

    path('filter-order/', views.filter_order, name='driver-filter-order'),
    path('clean-filter', views.clean_filter, name='driver-clean-filter'),

    path('accept-customer/<int:id>/', views.accept_customer, name='driver-accept-customer'),
    path('sucess/<int:id>/', views.success_order, name='driver-success-order'),
]
