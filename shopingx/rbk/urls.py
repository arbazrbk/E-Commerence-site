from django.urls import path
from rbk import views

urlpatterns = [
    path('', views.home, name='home'),
    path('adress/', views.address, name='address'),
    path('addtocart/', views.addtocart, name='addtocart'),
    path('order/', views.order, name='order'),
    path('orders/', views.orders, name='orders'),
    path('profile/', views.profile, name='profile'),
    path('productdetail/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('buynow/', views.buynow, name='buynow'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('registration/', views.customerregistration, name='customerregistration'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('mobile/<slug:slug>/', views.mobile, name='mobile'),
]