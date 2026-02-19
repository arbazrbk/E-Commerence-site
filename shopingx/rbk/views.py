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
        context = self.get_context()
        return render(request, 'rbk/profile.html', context)

    def post(self, request):
        name = request.POST.get('inputName', '').strip()
        address = request.POST.get('inputAddress', '').strip()
        address2 = request.POST.get('inputAddress2', '').strip()
        city = request.POST.get('inputCity', '').strip()
        state = request.POST.get('inputState', '').strip()
        zipcode = request.POST.get('inputZip', '').strip()
        messages = []
        if not name or not address or not city or not state or not zipcode:
            messages.append('Please fill all required fields.')
        else:
            # Always create a new Customer address for the current user
            from .models import Customer
            Customer.objects.create(
                User=request.user,
                name=name,
                locality=address,
                state=state,
                zipcode=zipcode
            )
            messages.append('New address added successfully!')
        context = self.get_context()
        context.update({
            'form_data': {
                'inputName': name,
                'inputAddress': address,
                'inputAddress2': address2,
                'inputCity': city,
                'inputState': state,
                'inputZip': zipcode,
            },
            'messages': messages
        })
        return render(request, 'rbk/profile.html', context)

    def get_context(self):
        topwear = Product.objects.filter(category='topwear')
        bottomwear = Product.objects.filter(category='bottomwear')
        mobile = Product.objects.filter(category='mobile')
        laptop = Product.objects.filter(category='laptop')
        return {
            'topwear': topwear,
            'bottomwear': bottomwear,
            'mobile': mobile,
            'laptop': laptop
        }

    def post(self, request):
        # Handle POST data here if needed
        return self.get(request)


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
        return redirect('emptycart') 
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
    custid = request.GET.get('custid')
    cart = Cart.objects.filter(user=user)
    for c in cart:
        orderplace(user=user, customer_id=custid, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('orders')    

@login_required                                      
def buynow(request):
    return render(request,'rbk/buynow.html')

@login_required
def changepassword(request):
    return render(request,'rbk/changepassword.html')


def LoginView(request):  
        return render(request,'rbk/login.html')

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
    def get(self,request):
        foam = Registrationforms()
        return render(request,'rbk/customerregistration.html',{'form':foam})
    
    def post(self,request):
        form = Registrationforms(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! Registered Successfully')
        return render(request,'rbk/customerregistration.html',{'form':form})

@login_required
def profile(request):
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