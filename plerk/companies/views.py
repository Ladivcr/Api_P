from django.shortcuts import render
from rest_framework import viewsets
from .models import Companies
from .serializers import CompaniesSerializer

# Create your views here.
class CompaniesViewSet(viewsets.ModelViewSet):
    serializer_class = CompaniesSerializer
    queryset = Companies.objects.all()
    #print(queryset)
