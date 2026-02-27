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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render
from .models import Product

class profileview(LoginRequiredMixin, View):
    def get(self, request):
        # Show the profile form with existing data if available
        try:
            customer = Customer.objects.get(User=request.user)
            form = Registrationforms(instance=customer)
        except Customer.DoesNotExist:
            form = Registrationforms()
        return render(request, 'rbk/profile.html', {'form': form})

    def post(self, request):
        # Save or update the profile data
        try:
            customer = Customer.objects.get(User=request.user)
            form = Registrationforms(request.POST, instance=customer)
        except Customer.DoesNotExist:
            form = Registrationforms(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.User = request.user
            customer.save()
            messages.success(request, 'Profile updated successfully!')
        else:
            messages.error(request, 'Please correct the errors below.')
        return render(request, 'rbk/profile.html', {'form': form})


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user = request.user)).exists()
        return render(request, 'rbk/productdetail.html', {'product': product,'item_already_in_cart': item_already_in_cart})
    
@login_required
def address(request):
    user = request.user
    ad = Customer.objects.filter(User=user)
    return render(request,'rbk/address.html', {'ad': ad,'active': 'btn-primary'})

@login_required
def addtocart(request): 
    user = request.user 
    product_id = request.GET.get('product_id') 
    if not product_id: 
        messages.error(request, 'No product selected to add to cart.') 
        return redirect('showcart') 
    try: 
        
        product = Product.objects.get(id=product_id) 
        cart, created = Cart.objects.get_or_create(user=user, product=product)
        if not created:
            cart.quantity += 1
        cart.save()
        # cart = Cart.objects.filter(Q(product=product_id) & Q(user=user))
        # if cart.exists():
        #     cart_item = cart.first()
        #     cart_item.quantity += 1
        #     cart_item.save()
        # else    
        # Cart(user=user, product_id=product_id).save() 
        messages.success(request, 'Product added to cart successfully.') 
    except Product.DoesNotExist: 
        messages.error(request, 'Product does not exist.') 
        return redirect('emptycart') 
    return redirect('showcart') 


def showcart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount =0.0
        shipingamount = 70.0
        totalamount = 0.0
        # cart_product = [c.product for c in cart]
        if cart:
            for c in cart:
                tempamount = (c.quantity * c.product.discounted_price)
                amount += tempamount
            totalamount = amount + shipingamount
            return render(request,'rbk/addtocart.html', {'carts': cart, 'totalamount': totalamount , 'amount': amount,'shipingamount': shipingamount})
        else:
            return render(request,'rbk/emptycart.html')
    else :
        return render(request,'rbk/emptycart.html')
        
def plus_cart(request):
    if request.method == 'GET':
        user = request.user
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        cart, created = Cart.objects.get_or_create(user=user, product=product)
        if not created:
            cart.quantity += 1
        cart.save()
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
                
            }
            return redirect('showcart')
        
def minus_cart(request):
        if request.method == 'GET':
           user = request.user 
           prod_id = request.GET['prod_id']
           cart = Cart.objects.get(Q(product=prod_id) & Q(user=user))
           if cart.quantity >1:  
              cart.quantity -= 1
              cart.save()
           else:
               cart.delete() 
           amount = 0.0     
           shipingamount = 70.0
           totalamount = 0.0
           cart_product = [p for p in Cart.objects.all() if p.user == request.user]
           for p in cart_product:
               tempamount = (p.quantity * p.product.discounted_price)
               amount += tempamount
               totalamount = amount + shipingamount
            
               data = {
                'quantity': cart.quantity,
                'amount': amount,
                 'totalamount': totalamount
                }
               return redirect('showcart') 
         
def remove_cart(request):
        if request.method == 'GET':
           prod_id = request.GET['prod_id']
           c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
           c.delete()
           return redirect('showcart')  

@login_required                              
def paymentdone(request):
    user = request.user
    custid = request.POST.get('custid') or request.GET.get('custid')
    cart = Cart.objects.filter(user=user)
    for c in cart:
        print(c.product, c.quantity)
        orderplace(user=user, customer_id=custid, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('payment_success')

def payment_success(request):
    return render(request,'rbk/payment_successful.html')

@login_required                                      
def buynow(request):
    return render(request,'rbk/buynow.html')

@login_required
def changepassword(request):
    user = request.user
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('changepassword')

        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.')
            return redirect('changepassword')

        user.set_password(new_password)
        user.save()
        messages.success(request, 'Password changed successfully. Please log in again.')
        logout(request)
        return redirect('login')
    
    return render(request,'rbk/changepassword.html')


def LoginView(request):
    if request.method == 'POST':
        form = Loginforms(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = Loginforms()
    return render(request, 'rbk/login.html', {'form': form})

@login_required
def topwear(request,data=None):
    if data is None:
        topwears = Product.objects.filter(category='topwear')
    elif data in ['Adidas', 'Nike']:
        topwears = Product.objects.filter(category='topwear', brand=data)
    else:
        topwears = Product.objects.filter(category='topwear')
    return render(request, 'rbk/topwear.html', {'topwears': topwears}) 

@login_required
def bottomwear(request,data=None):
    if data is None:
        bottomwears = Product.objects.filter(category='bottomwear')
    elif data in ['Adidas', 'Nike']:
        bottomwears = Product.objects.filter(category='bottomwear', brand=data)
    else:
        bottomwears = Product.objects.filter(category='bottomwear')
    return render(request, 'rbk/bottomwear.html', {'bottomwears': bottomwears})

@login_required   
def laptop(request,data=None):
    if data is None:
        laptops = Product.objects.filter(category='laptop')
    elif data in ['HP', 'DELL']:
        laptops = Product.objects.filter(category='laptop', brand=data)
    else:
        laptops = Product.objects.filter(category='laptop')
    return render(request, 'rbk/laptop.html', {'laptops': laptops})          

@login_required
def mobile(request,data=None):
    if data is None:
        mobiles = Product.objects.filter(category='mobile')
    elif data in ['Redmi', 'Samsung']:
        mobiles = Product.objects.filter(category='mobile', brand=data)
    else:
        mobiles = Product.objects.filter(category='mobile')
    return render(request, 'rbk/mobile.html', {'mobiles': mobiles})



class customerregistration(View):
    def get(self, request):
        form = Registrationforms()
        return render(request, 'rbk/customerregistration.html', {'form': form})

    def post(self, request):
        form = Registrationforms(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        # You can add email or other fields as needed
        if form.is_valid() and email and password:
            try:
                with transaction.atomic():
                    user = User.objects.create_user(username=email, password=password)
                    customer = form.save(commit=False)
                    customer.User = user
                    customer.save()
                messages.success(request, 'Congratulations!! Registered Successfully')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Registration failed: {e}')
        else:
            messages.error(request, 'Please fill all fields correctly.')
        return render(request, 'rbk/customerregistration.html', {'form': form})

@login_required
def home(request):
    return render(request,'rbk/home.html')

@login_required
def orders(request):
    user = request.user
    orders = orderplace.objects.filter(user=user)
    return render(request, 'rbk/orders.html', {'orders': orders})

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(User = user)
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

def emptycart(request):
    return render(request,'rbk/emptycart.html')



def logout_view(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
    return redirect('login')

def search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Product.objects.filter(title__icontains=query)
    return render(request, 'rbk/search_results.html', {'results': results, 'query': query})

from django.db.models import Q

def get_related_products(product):
    # Recommend products from same category, excluding current product
    return Product.objects.filter(Q(category=product.category) & ~Q(id=product.id))[:4]

from django import template
register = template.Library()

@register.filter
def get_related_products(product):
    return get_related_products(product)

