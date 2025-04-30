from django.db import models

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True, null=True)
    image_urls = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class User(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=50, unique=True, null=False, blank=False)
    phone = models.CharField(max_length=20, unique=True, null=False, blank=False)
    user_type = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('customer', 'Customer')], default='customer')

    def __str__(self):
        return self.user_name
    
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    buyer_phone = models.CharField(max_length=100, null=True, blank=True)  # Ensure this field exists
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField(default=0)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.product.name} x {self.quantity}"
    