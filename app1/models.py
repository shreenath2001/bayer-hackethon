from django.db import models
from datetime import datetime
# Create your models here.

class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(blank = True, default = datetime.now)

    def __str__(self):
        return self.email

class OrderUpdate(models.Model):
    update_id= models.AutoField(primary_key=True)
    order_id= models.IntegerField(default="")
    update_desc= models.CharField(max_length=5000)
    arrived = models.CharField(max_length=5000)
    dispatched = models.CharField(max_length=5000)
    arrived_date = models.CharField(max_length=5000, default="")
    dispatched_date = models.CharField(max_length=5000, default="")
    arrived_time = models.CharField(max_length=5000, default="")
    dispatched_time = models.CharField(max_length=5000, default="")
    timestamp= models.DateField(auto_now_add= True)

class authenticator(models.Model):
    auth_secret = models.CharField(max_length=100)
    claimed = models.BooleanField(default=False)
    created_at = models.DateTimeField(blank = True, default = datetime.now)

class Claimed(models.Model):
    auth_secret = models.CharField(max_length=100)

def __str__(self):
    return self.update_desc[0:7] + "..."
