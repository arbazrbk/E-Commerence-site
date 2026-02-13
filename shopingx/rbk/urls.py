from django.urls import path 
from rbk import  views 

urls_pattern = {
    path('',views.home,name='home'),
    path('adress/',views.address,name='address'),
    path('add/',views.addtocart,name='addtocart'),
    path('order/',views.order,name='order'),
    path('profile/',views.profile,name='profile'),
    path('productdetail/',views.productdetail,name='productdetail'),
    path('buynow/',views.buynow,name='buynow'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('login/',views.login,name='login'),
    path('registration/',views.customerregistration,name='customerregistration'),
    
} 