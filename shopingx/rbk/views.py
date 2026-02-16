from django.shortcuts import render
from .models import customer, Product, Cart
from django.views import View

class profileview(View):
    def get(self):
        topwear = Product.onject.filter(category='topwear')
        bottomwear = Product.onject.filter(category='bottomwear')
        mobile = Product.onject.filter(category='mobile')
        laptop = Product.onject.filter(category='laptop')
        return render(self.request,'rbk/profile.html',{'topwear':topwear,'bottomwear':bottomwear,'mobile':mobile,'laptop':laptop})
def home(request):
    return render(request,'rbk/home.html')

def address(request):
    return render(request,'rbk/address.html')

def addtocart(request):
    return render(request,'rbk/addtocart.html')

def buynow(request):
    return render(request,'rbk/buynow.html')

def changepassword(request):
    return render(request,'rbk/changepassword.html')

def login (request):
    return render(request,'rbk/login.html')

def mobile(request):
    return render(request,'rbk/mobile.html')

def customerregistration(request):
    return render(request,'rbk/customerregistration.html')

def productdetail(request):
    return render(request,'rbk/productdetail.html')

def order(request):
    return render(request,'rbk/order.html')

def profile(request):
    return render(request,'rbk/profile.html')

def orders(request):
    return render(request, 'rbk/orders.html')