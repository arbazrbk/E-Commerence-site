from django.shortcuts import render

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

def productdetail(request):
    return render(request,'rbk/productdetail.html')

def profile(request):
    return render(request,'rbk/profile.html')