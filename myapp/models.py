from django.db import models

# Create your models here.

class new_crud(models.Model):
    id=models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=50,null=True)
    email=models.CharField(max_length=20,default='user@gmail.com')
    phone=models.CharField(max_length=10,unique=True)
    profile_url=models.URLField(blank=True, null=True)