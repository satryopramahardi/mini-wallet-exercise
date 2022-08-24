from pyexpat import model
from rest_framework import serializers
from .models import Customer, Wallet, BalanceRecord


class CustomerInitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["xid"]
    
    def validate_id(self, value):
        if len(str(value)) != 36:
            raise serializers.ValidationError('customer_xid not valid (must be 36 char)')
        return value

class CreateWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["id", "owned_by"]

class DisableWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["id", "owned_by", "balance", 'status', 'disabled_at']


class EnableWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["id", "owned_by", "enabled_at", "balance", 'status']

class WalletBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Wallet
        fields = ['balance']

class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceRecord
        fields = ['reference_id','owned_by','transaction_type','transaction_date','amount','wallet','status']
