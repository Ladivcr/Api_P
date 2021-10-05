from rest_framework import serializers
from transactions.models import Transactions
from companies.models import Companies

class Post1Serializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = "__all__"
        
class Post2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Companies
        fields = "__all__"
