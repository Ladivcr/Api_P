from django.db import models

# Create your models here.
import uuid
# Create your models here.
class Companies(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    status = models.CharField(max_length=8, blank=False, default="activa")
    # Es la longitud más grande de los ID generados aleatoriamente en el preprocesamiento
    ID = models.CharField(primary_key = True, max_length=36, unique=True) 

    def __str__(self): 
        return (str(self.ID))