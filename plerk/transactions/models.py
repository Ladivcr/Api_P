from django.db import models

# Create your models here.


# Create your models here.
from companies.models import Companies

class Transactions(models.Model):
    ID = models.CharField(primary_key = True, max_length=36, unique=True)
    ID_Company = models.ForeignKey(Companies, on_delete=models.CASCADE)
    price = models.FloatField(blank=False)
    transaction_date = models.DateTimeField(blank=False)
    status_transaction = models.CharField(max_length=8, blank=False)
    status_approved = models.BooleanField(blank=False)
    final_pay = models.CharField(max_length=1, blank=False)


    def __str__(self): 
        return (str(self.ID))