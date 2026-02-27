from django import template
from rbk.models import Product
from django.db.models import Q

register = template.Library()

@register.filter
def get_related_products(product):
    return Product.objects.filter(Q(category=product.category) & ~Q(id=product.id))[:4]
