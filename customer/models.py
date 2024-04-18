from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.




class User(AbstractUser):
    address = models.TextField(default = 'No address')
class Item(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField()
    image = models.ImageField()
    price = models.DecimalField(max_digits = 5, decimal_places = 2)
    category = models.ManyToManyField('Category', related_name = 'item')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default = 0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

class OrderItem(models.Model):
    product = models.ForeignKey(Item, on_delete=models.CASCADE)    
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default = True)   
 
    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

class Order(models.Model):
    order_items = models.ManyToManyField('OrderItem', related_name = 'item')
    total_price = models.DecimalField(max_digits = 7, decimal_places = 2, default = 0.00)
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    date_added = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default = False)
 
    def __str__(self):
        return f'{self.date_added}'        
# models.py



class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



