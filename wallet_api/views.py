from functools import partial
import logging
from datetime import datetime
from .serializers import CustomerInitSerializer,EnableWalletSerializer,\
    DisableWalletSerializer,CreateWalletSerializer,BalanceSerializer,WalletBalanceSerializer
from .utils import generate_wallet_id, generate_response
from .models import Customer, Wallet,BalanceRecord
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token

from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny

from .serializers import *

logger = logging.getLogger(__name__)


@api_view(["POST"])
@permission_classes([AllowAny])
def initialize_customer_api( request, *args, **kwargs):
    try:
        customer = Customer.objects.get(xid=request.data['customer_xid'])
    except:
        customer = None

    if not customer:
        serializer = CustomerInitSerializer(data=dict(xid=request.data['customer_xid']))
        if serializer.is_valid():
            # Debug only: username=password=xid
            User.objects.create_user(
                username=serializer.validated_data['xid'],
                password=serializer.validated_data['xid']
            )
            serializer.save()
        # Debug only: if customer already exist, return the token value
        else:
            return Response(generate_response(data=serializer.errors,success=False), status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.get(username=request.data['customer_xid'])

    wallet_serializer = CreateWalletSerializer(data=dict(
        id = generate_wallet_id(),
        owned_by=Customer.objects.get(xid=request.data['customer_xid']),
    ))

    if wallet_serializer.is_valid():
        wallet_serializer.save()

    data = dict(Token=str(Token.objects.get(user=user)))
    return Response(generate_response(data=data,success=True), status=status.HTTP_200_OK)

@api_view(["POST","GET","PATCH"])
def wallet_api(request, *args, **kwargs):
    auth_token = Token.objects.get(key=request.META['HTTP_AUTHORIZATION'].split(' ')[1])
    try:
        customer = Customer.objects.get(xid=auth_token.user)
        wallet = Wallet.objects.get(owned_by_id=customer)
    except:
        return Response(generate_response(data={"message":"Can't retrieve wallet"},success=False), status=status.HTTP_400_BAD_REQUEST)
    
    if request.method=="GET":
        serializer = EnableWalletSerializer(instance=wallet)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    if request.method=="POST":
        if wallet.status=='enabled':
            return Response(generate_response(data={"message":"Wallet is already enabled"},success=False), status=status.HTTP_400_BAD_REQUEST)
        serializer=EnableWalletSerializer(wallet,data=dict(
            id=wallet.id,
            owned_by=customer,
            status="enabled",
            enabled_at=datetime.now(),
            balance=wallet.balance,
            disabled_at=None
        ),partial=True)
    if request.method=="PATCH":
        if wallet.status=='disabled':
            return Response(generate_response(data={"message":"Wallet is already disabled"},success=False), status=status.HTTP_400_BAD_REQUEST)
        serializer = DisableWalletSerializer(wallet,data=dict(
            id=wallet.id,
            owned_by=customer,
            status="disabled",
            disabled_at=datetime.now(),
            balance=wallet.balance,
            enabled_at=None
        ),partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    return Response(generate_response(data={"message":serializer.errors },success=False), status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def deposit_api(request, *args, **kwargs):
    success=False
    auth_token = Token.objects.get(key=request.META['HTTP_AUTHORIZATION'].split(' ')[1])
    try:
        customer = Customer.objects.get(xid=auth_token.user)
        wallet = Wallet.objects.get(owned_by_id=customer)
    except:
        return Response(generate_response(data={"message":"Can't retrieve wallet"},success=False), status=status.HTTP_400_BAD_REQUEST)

    balance = wallet.balance
    if wallet.status=="enabled":
        success=True
        balance += float(request.data.get('amount'))

    wallet_serializer=WalletBalanceSerializer(wallet,data=dict(balance=balance),partial=True)
   
    serializer = BalanceSerializer(data=dict(
        reference_id = request.data.get('reference_id'),
        transaction_type = "Deposit",
        transaction_date = datetime.now(),
        amount=request.data.get('amount'),
        status="Success" if success else "Failed",
        owned_by=customer,
        wallet=wallet
    ))

    if serializer.is_valid():
        if wallet_serializer.is_valid():
            wallet_serializer.save()
        else:
            return Response(generate_response(data={"message":wallet_serializer.errors},success=False), status=status.HTTP_400_BAD_REQUEST)
    
        serializer.save()
        data = dict(
            id=serializer.validated_data['wallet'],
            deposited_by=serializer.validated_data['owned_by'],
            status=serializer.validated_data['status'],
            deposited_at=serializer.validated_data['transaction_date'],
            amount=serializer.validated_data['amount'],
            reference_id=serializer.validated_data['reference_id'],
        )
        return Response(generate_response(data=serializer.data,success=True), status=status.HTTP_200_OK)
    else:
        return Response(generate_response(data={"message":serializer.errors},success=False), status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def withdrawal_api(request, *args, **kwargs):
    success=False
    auth_token = Token.objects.get(key=request.META['HTTP_AUTHORIZATION'].split(' ')[1])
    try:
        customer = Customer.objects.get(xid=auth_token.user)
        wallet = Wallet.objects.get(owned_by_id=customer)
    except:
        return Response(generate_response(data={"message":"Can't retrieve wallet"},success=False), status=status.HTTP_400_BAD_REQUEST)

    balance = wallet.balance
    if wallet.balance >= float(request.data.get('amount')) and wallet.status=="enabled":
        success=True
        balance -=float(request.data.get('amount'))

    wallet_serializer=WalletBalanceSerializer(wallet,data=dict(balance=balance),partial=True)
    serializer = BalanceSerializer(data=dict(
        reference_id = request.data.get('reference_id'),
        transaction_type = "Withdrawal",
        transaction_date = datetime.now(),
        amount=request.data.get('amount'),
        status="Success" if success else "Failed",
        owned_by=customer,
        wallet=wallet
    ))

    if serializer.is_valid():
        if wallet_serializer.is_valid():
            if success:
                wallet_serializer.save()
        else:
            return Response(generate_response(data={"message":wallet_serializer.errors},success=False), status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        data = dict(
            id=serializer.validated_data['wallet'],
            deposited_by=serializer.validated_data['owned_by'],
            status=serializer.validated_data['status'],
            deposited_at=serializer.validated_data['transaction_date'],
            amount=serializer.validated_data['amount'],
            reference_id=serializer.validated_data['reference_id'],
        )
        return Response(generate_response(data=serializer.data,success=True), status=status.HTTP_200_OK)
    else:
        return Response(generate_response(data={"message":serializer.errors},success=False), status=status.HTTP_400_BAD_REQUEST)
