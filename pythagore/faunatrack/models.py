from django.db import models
from django.contrib.auth.models import User
# from django.utils.translation import gettext_lazy as _

# Create your models here.
# class Guitare(models.Model):
#     marque = models.CharField(max_length=255, default="", verbose_name="marque_guitare")
#     nom = models.CharField(max_length=255, default="")

class Espece(models.Model):

    class StatusChoice(models.TextChoices):
        # DANS_MON_CODE = ("NOM_EN_BDD", "Nom affiché à l'utilisateur")
        EN_DANGER = ("DANGER", "En voie de disparition")
        EN_FORME = ("OK", "Espèce non menacé")

    nom = models.CharField(max_length=255, default="", verbose_name="Nom de l'espèce")
    status = models.CharField(choices=StatusChoice.choices, verbose_name="status de l'espèce", default=StatusChoice.EN_FORME, max_length=255)

    def __str__(self):
        return self.nom


class Projet(models.Model):
    titre = models.CharField(max_length=255, verbose_name="Titre du projet", default="Projet sans titre")
    description = models.TextField(verbose_name="Description du projet", null=True, blank=True, default=None )
    scientifiques = models.ManyToManyField("faunatrack.ProfilScientifique", related_name="projets")
    date_creation = models.DateField(auto_now_add=True)
    date_maj = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.titre

class GPS(models.Model):
    latitude = models.DecimalField(decimal_places=5, max_digits=8)
    longitude = models.DecimalField(decimal_places=5, max_digits=8)

    class Meta:
        verbose_name="GPS"
        verbose_name_plural = "GPS"

    def __str__(self):
        return f"Un endroit super cool avec les coordonnées suivantes: {self.latitude}, {self.longitude}"

class Observation(models.Model):
    scientifique = models.ForeignKey("faunatrack.ProfilScientifique", on_delete=models.SET_NULL, related_name="observations", null=True, default=None)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name="observations", null=True, default=None)
    espece = models.ForeignKey(Espece, on_delete=models.PROTECT, related_name="observations")
    quantite = models.IntegerField(default=0)
    date_observation = models.DateTimeField()
    notes = models.TextField(default="Pas de notes pour cette observation")
    photo = models.ImageField(upload_to="faunatrack/static/photo_observations", blank=True, null=True, default=None )
    emplacement = models.ForeignKey(GPS, on_delete=models.SET_NULL, related_name="observations", null=True, default=None)

    def __str__(self):
        return f"{self.espece} observé à: {self.emplacement.latitude}, {self.emplacement.longitude}, le {self.date_observation}"

# class UserFaunatrack(User):
#     pass     

class ProfilScientifique(models.Model):
    user = models.OneToOneField(User, related_name="profil_scientifique", on_delete=models.CASCADE)
    domaine_de_recherche = models.CharField(max_length=255, default="")

    class Meta:
        verbose_name="Profil scientifique"
        verbose_name_plural = "Profils scientifique"

    def __str__(self):
        return self.user.username