from django.urls import path
from rbk import views

urlpatterns = [
    path('', views.profileview.as_view(), name='home'),
    path('adress/', views.address, name='address'),
    path('addtocart/', views.addtocart, name='addtocart'),
    path('showcart/', views.showcart, name='showcart'),
    path('pluscart/', views.plus_cart, name='plus_cart'),
    path('minuscart/', views.minus_cart, name='minus_cart'),
    path('removecart/', views.remove_cart, name='remove_cart'),
    path('orders/', views.orders, name='orders'),
    path('profile/', views.profile, name='profile'),
    path('productdetail/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('buynow/', views.buynow, name='buynow'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('login/', views.LoginView, name='login'),
    path('registration/', views.customerregistration.as_view(), name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.paymentdone, name='paymentdone'),
    path('mobile/', views.mobile, name='mobile'),
]