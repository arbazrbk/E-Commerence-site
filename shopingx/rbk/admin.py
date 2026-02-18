from django.contrib import admin
from .models import Customer, Product, Cart, orderplace

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','name','locality','zipcode','state']   
    
@admin.register(Product)
class Productadmin(admin.ModelAdmin):    
    list_display = ['id','product_id','title','selling_price','discounted_price','description','brand','category','product_image']    

@admin.register(Cart)
class Cartadmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']
    
@admin.register(orderplace)
class OrderPlacedadmin(admin.ModelAdmin):
    list_display = ['id','user','customer','product','quantity','ordered_date','status']    
    
    