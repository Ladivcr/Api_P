from django.db import models
from rest_framework import serializers
from .models import Companies

class CompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companies
        fields = "__all__"
