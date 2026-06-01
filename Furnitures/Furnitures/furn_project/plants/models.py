from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username
    
    
from django.db import models
from django.contrib.auth.models import User

# 🌱 Plant Model
class Plant(models.Model):
    plant_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    info = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='plants/')
    plant_type = models.CharField(max_length=100, default='Sapling')
    growth = models.CharField(max_length=50)  # e.g. 5 months / 10 months
    quality = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name


# 👤 Profile Model (User Contact)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

from django.db import models
from django.contrib.auth.models import User
from .models import Plant
from datetime import timedelta, datetime

PAYMENT_CHOICES = (
    ('online', 'Online'),
    ('offline', 'Offline'),
)

ORDER_STATUS = (
    ('pending', 'Pending'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
)

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    
    # User details
    first_name = models.CharField(max_length=50, default="N/A")
    last_name = models.CharField(max_length=50, default="N/A")
    contact = models.CharField(max_length=15, default="0000000000")
    
    # Address details
    address = models.TextField(default="N/A")
    state = models.CharField(max_length=50, default="N/A")
    district = models.CharField(max_length=50, default="N/A")
    location = models.CharField(max_length=50, default="N/A")
    pincode = models.CharField(max_length=10, default="000000")
    
    # Payment
    pay_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='offline')
    quantity = models.PositiveIntegerField(default=1)
    # Booking info
    booking_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(default=datetime.now() + timedelta(days=4))
    status = models.CharField(max_length=10, choices=ORDER_STATUS, default='pending')

    def __str__(self):
        return f"{self.user.username} - {self.plant.name}"

# 🛒 AddToCart Model
class AddToCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'plant')  # One plant per user in cart

    def __str__(self):
        return f"{self.user.username} - {self.plant.name} ({self.quantity})"
    
    
# 🌿 Contact Model
class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"