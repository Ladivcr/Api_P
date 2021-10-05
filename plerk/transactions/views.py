from django.shortcuts import render
from rest_framework import viewsets
from .models import Transactions
from .serializers import TransactionsSerializer
from rest_framework.decorators import action

# Create your views here.

class TransactionsViewSet(viewsets.ModelViewSet):
    serializer_class =TransactionsSerializer
    queryset = Transactions.objects.all()


    
