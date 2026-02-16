from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

State_choices=(
    ('karachi','karachi'),
    ('islamabad','islamabad'),
    ('pindi','pindi'),
    ('queta','queta'),
    ('gilgit','gilgit'),
    ('hunza','hunza'),
    ('ghizer','ghizer'),
    ('yasin','yasin'),
)

class customer(models.Model):
    User = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    locality = models.CharField(max_length=100)
    zipcode = models.IntegerField(validators=[MinValueValidator(10000), MaxValueValidator(99999)])
    state = models.CharField(choices=State_choices,max_length=100)

def __str__(self):
    return str(self.id)

Category_choices =(
    ('mobile','mobile'),
    ('laptop','laptop'),
    ('topwear','topwear'),
    ('bottomwear','bottomwear')
        
)

class Product(models.Model):
    product_id = models.CharField(max_length=100)
    tiltle = models.CharField(max_length = 200)
    selling_price = models.FloatField(max_length=200)
    discounted_price = models.FloatField(max_length=100)
    description = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    category = models.CharField(choices=Category_choices,max_length=100)
    product_image = models.ImageField()
    
def __str__(self):
    return str(self.product_id)

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

def __str__(self):
    return str(self.id)


Status_choices = (
    ('pending','pending'),
    ('delivered','delivered'),
    ('cancel','cancel'),
)

class orderplace(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=Status_choices,default='Pending')
    
def __str__(self):
    return str(self.id)    


