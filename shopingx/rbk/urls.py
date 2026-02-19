
from django.urls import path
from rbk import views

urlpatterns = [
    path('home/', views.profile, name='home'),
    path('address/', views.address, name='adress'),
    path('addtocart/', views.addtocart, name='addtocart'),
    path('showcart/', views.showcart, name='showcart'),
    path('removecart/', views.remove_cart, name='removecart'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('orders/', views.orders, name='orders'),
    path('profile/', views.profileview.as_view(), name='profile'),
    path('productdetail/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('buynow/', views.buynow, name='buynow'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('login/', views.LoginView, name='login'),
    path('registration/', views.customerregistration.as_view(), name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.paymentdone, name='paymentdone'),
    path('mobile/', views.mobile, name='mobile'),
    path('laptop/', views.laptop, name='laptop'),
    path('topwear/', views.topwear, name='topwear'),
    path('bottomwear/', views.bottomwear, name='bottomwear'),
    path('emptycart/', views.emptycart, name='emptycart'),
]