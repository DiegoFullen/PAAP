from django.db import models
from django.contrib.auth.hashers import make_password

class User(models.Model):
    email = models.EmailField(primary_key=True) 
    username = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128) 
    email_recover = models.EmailField()
    status = models.BooleanField()

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

class Dataset(models.Model):
    id_dataset = models.IntegerField(primary_key=True)
    email = models.ForeignKey(User, on_delete=models.CASCADE) 
    upload_date = models.CharField(max_length=15)
    name_dataset = models.CharField(max_length=50)
    size = models.DecimalField(max_digits=20, decimal_places=6)

class Model(models.Model):
    id_model = models.IntegerField(primary_key=True)
    id_dataset = models.IntegerField()
    start_date = models.CharField(max_length=15)
    finish_date = models.CharField(max_length=15)
    name = models.CharField(max_length=50)
    type = models.IntegerField()

class Plan(models.Model):
    email = models.ForeignKey(User, on_delete=models.CASCADE)  
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    type_plan = models.IntegerField()
