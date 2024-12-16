from django.db import models

# Create your models here.
# class Guitare(models.Model):
#     marque = models.CharField(max_length=255, default="", verbose_name="marque_guitare")
#     nom = models.CharField(max_length=255, default="")

class Espece(models.Model):
    nom = models.CharField(max_length=255, default="", verbose_name="nom_espece")