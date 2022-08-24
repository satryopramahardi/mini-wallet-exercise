from pyexpat import model
from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    xid = models.CharField(max_length=36, primary_key=True,validators=[MinLengthValidator])
    created_at = models.DateTimeField(auto_now=True)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_customer(sender, instance, created, **kwargs):
        if created:
            Token.objects.create(user=instance)
    
    def __str__(self) -> str:
        return self.xid


class Wallet(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    owned_by = models.ForeignKey(Customer, on_delete= models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=25, default="disabled",  null=True)
    enabled_at = models.DateTimeField( null=True)
    disabled_at = models.DateTimeField( null=True)
    balance = models.FloatField(default=0.0)


    def __str__(self) -> str:
        return self.id


class BalanceRecord(models.Model):
    reference_id = models.CharField(max_length=36, primary_key=True, validators=[MinLengthValidator])
    transaction_type = models.CharField(max_length=20, null=True)
    transaction_date = models.DateTimeField(null=True)
    amount=models.FloatField(null=True)
    status=models.CharField(max_length=20,default="Failed")
    owned_by = models.ForeignKey(Customer, on_delete= models.CASCADE, blank=True, null=True)
    wallet=models.ForeignKey(Wallet,on_delete= models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return self.reference_id
