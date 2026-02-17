from django.http import JsonResponse
from django.shortcuts import render
from .models import customer, Product, Cart
from django.views import View
from .forms import Registrationforms, Loginforms
from django.contrib import messages
from django.db.models import Q

class profileview(View):
    def get(self, request):
        topwear = Product.objects.filter(category='topwear')
        bottomwear = Product.objects.filter(category='bottomwear')
        mobile = Product.objects.filter(category='mobile')
        laptop = Product.objects.filter(category='laptop')
        return render(request, 'rbk/profile.html', {
            'topwear': topwear,
            'bottomwear': bottomwear,
            'mobile': mobile,
            'laptop': laptop
        })


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'rbk/productdetail.html', {'product': product})
    
    
def home(request):
    return render(request,'rbk/home.html')

def address(request):
    ad = customer.objects.filter(user=request.user)
    return render(request,'rbk/address.html', {'ad': ad,'active': 'btn-primary'})

def addtocart(request):
    user = request.user
    product_id = request.Get.get('Product_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product_id=product).save()
    return render(request,'rbk/addtocart.html')

def showcart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount =0.0
        shipingamount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
            totalamount = amount + shipingamount
            return render(request,'rbk/addtocart.html', {'cart': cart, 'totalamount': totalamount , 'amount': amount})
        else:
            return render(request,'rbk/emptycart.html')
        
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipingamount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            totalamount = amount + shipingamount
            
            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': totalamount
            }
            return JsonResponse(data) 
        
def minus_cart(request):
        if request.method == 'GET':
           prod_id = request.GET['prod_id']
           c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
           c.quantity -= 1
           c.save()
           amount = 0.0
           shipingamount = 70.0
           totalamount = 0.0
           cart_product = [p for p in Cart.objects.all() if p.user == request.user]
           for p in cart_product:
               tempamount = (p.quantity * p.product.discounted_price)
               amount += tempamount
               totalamount = amount + shipingamount
            
               data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': totalamount
                }
               return JsonResponse(data)       
def buynow(request):
    return render(request,'rbk/buynow.html')

def changepassword(request):
    return render(request,'rbk/changepassword.html')

class LoginView(View):
    def get(self,request):
      return render(request,'rbk/login.html')
  
    def get(self,request):
        form = Loginforms()
        return render(request,'rbk/login.html',{'form':form})
    
    def post(self,request):
        form = Loginforms(request.POST)
        if form.is_valid():
            messages.sucess(request,'Congratulations!! Login Successfully')
            form.save()
        return render(request,'rbk/login.html',{'form':form})

          

def mobile(request,data=None):
    if data == None:
       mobile = Product.object.filter(category='mobile')
    elif data == 'Redmi' or data == 'Samasung':
        mobile = Product.object.filter(category='mobile').filter(brand=data)   
    return render(request,'rbk/mobile.html',{'mobile':mobile})

class customerregistration(View):
    def get(self,request):
        foam = Registrationforms()
        return render(request,'rbk/customerregistration.html',{'form':foam})
    
    def post(self,request):
        form = Registrationforms(request.POST)
        if form.is_valid():
            messages.sucess(request,'Congratulations!! Registered Successfully')
        return render(request,'rbk/customerregistration.html',{'form':form})
def productdetail(request):
    return render(request,'rbk/productdetail.html')

def order(request):
    return render(request,'rbk/order.html')

def profile(request):
    return render(request,'rbk/profile.html')

def orders(request):
    return render(request, 'rbk/orders.html')