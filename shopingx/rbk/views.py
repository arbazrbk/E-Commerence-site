from django.http import JsonResponse
from django.shortcuts import render
from .models import Customer, Product, Cart
from django.views import View
from .forms import Registrationforms, Loginforms
from django.contrib import messages
from django.db.models import Q
from .models import orderplace
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required



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
        item_already_in_cart = False
        item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user = request.user)).exists()
        return render(request, 'rbk/productdetail.html', {'product': product,'item_already_in_cart': item_already_in_cart})
    
@login_required
def address(request):
    ad = Customer.objects.filter(user=request.user)
    return render(request,'rbk/address.html', {'ad': ad,'active': 'btn-primary'})

@login_required
def addtocart(request):
    user = request.user
    product_id = request.GET.get('product_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product_id=product).save()
    return render(request,'rbk/addtocart.html')

@login_required
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
def remove_cart(request):
        if request.method == 'GET':
           prod_id = request.GET['prod_id']
           c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
           c.quantity -= 1
           c.delete()
           amount = 0.0
           shipingamount = 70.0
           totalamount = 0.0
           cart_product = [p for p in Cart.objects.all() if p.user == request.user]
           for p in cart_product:
               tempamount = (p.quantity * p.product.discounted_price)
               amount += tempamount
               totalamount = amount + shipingamount
            
               data = {
                'amount': amount,
                'totalamount': totalamount
                }
               return JsonResponse(data)  

                               
def paymentdone(request):
    user = request.user
    custid = request.GET.get('custid')
    cart = Cart.objects.filter(user=user)
    for c in cart:
        orderplace(user=user, customer_id=custid, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('orders')    
                                       
def buynow(request):
    return render(request,'rbk/buynow.html')

def changepassword(request):
    return render(request,'rbk/changepassword.html')

@method_decorator(login_required, name='dispatch')
def LoginView(request):  
        return render(request,'rbk/login.html')
    
          

def mobile(request,data=None):
    if data is None:
        mobiles = Product.objects.filter(category='mobile')
    elif data in ['Redmi', 'Samsung']:
        mobiles = Product.objects.filter(category='mobile', brand=data)
    else:
        mobiles = Product.objects.filter(category='mobile')
    return render(request, 'rbk/mobile.html', {'mobiles': mobiles})

class customerregistration(View):
    def get(self,request):
        foam = Registrationforms()
        return render(request,'rbk/customerregistration.html',{'form':foam})
    
    def post(self,request):
        form = Registrationforms(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! Registered Successfully')
        return render(request,'rbk/customerregistration.html',{'form':form})



def orders(request):
    user = request.user
    orders = orderplace.objects.filter(user=user)
    return render(request, 'rbk/orders.html', {'orders': orders})

def checkout(request):
    user = request.user
    add = Customer.objects.filter(user = user)
    cart_product = Cart.objects.filter(user=user)
    amount = 0.0
    shipingamount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount
        totalamount = amount + shipingamount
    return render(request, 'rbk/checkout.html', {'add': add, 'totalamount': totalamount, 'cart_product': cart_product})    