from django.db import models
from django.contrib.auth.models import User, Permission, Group
from django.core.mail import send_mail
from faunatrack.validators import validate_latitude, validate_longitude


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
    latitude = models.DecimalField(decimal_places=5, max_digits=8, validators=[validate_latitude])
    longitude = models.DecimalField(decimal_places=5, max_digits=8, validators=[validate_longitude])

    class Meta:
        verbose_name="GPS"
        verbose_name_plural = "GPS"

    def __str__(self):
        return f"Un endroit super cool avec les coordonnées suivantes: {self.latitude}, {self.longitude}"

class Observation(models.Model):
    scientifique = models.ForeignKey("faunatrack.ProfilScientifique", on_delete=models.SET_NULL, related_name="observations", null=True, blank=True, default=None)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name="observations", null=True, default=None)
    espece = models.ForeignKey(Espece, on_delete=models.PROTECT, related_name="observations")
    quantite = models.IntegerField(default=0)
    date_observation = models.DateTimeField()
    notes = models.TextField(default="Pas de notes pour cette observation")
    photo = models.ImageField(upload_to="faunatrack/static/photo_observations", blank=True, null=True, default=None )
    emplacement = models.ForeignKey(GPS, on_delete=models.SET_NULL, related_name="observations", null=True, default=None)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        total_quantite = Observation.objects.filter(espece=self.espece).aggregate(total=models.Sum("quantite"))["total"]
        if total_quantite and total_quantite < 10:
            self.espece.status = Espece.StatusChoice.EN_DANGER
        elif total_quantite and total_quantite >= 10:
            self.espece.status = Espece.StatusChoice.EN_FORME
        self.espece.save()

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
    
    def add_permissions_for_scientifique(self):
        permissions = Permission.objects.filter(content_type__app_label="faunatrack")
        for permission in permissions:
            self.user.user_permissions.add(permission)
        self.user.save()
        
    def add_pythagore_group(self):
        try:
            # Fix: group was "Pythagore" and not "pythagore" in my db
            pythagore_group = Group.objects.get(name='Pythagore')
            self.user.groups.add(pythagore_group)
            self.user.save()
        except Group.DoesNotExist:
            send_mail(
                "ERROR: Le group Pythagore n'a pas été créé en BDD !",
                "Merci d'ajouter le groupe Pythagore",
                "from@example.com",
                ["to@example.com"],
                fail_silently=False,
            ) 
            # Alternatives : Crée le groupe pythagore dans le code plutôt que dans l'admin: 
            # save method, signals, migrations....
        
        
    # Attention cette méthode est appelé dès que l'instance est modifié ET/OU créée! 
    def save(self, *args, **kwargs):
        if not self.pk: # Cas d'un AJOUT dans la bdd
            self.add_permissions_for_scientifique()
            self.add_pythagore_group()
        else: # Cas de modification en bdd
            pass
        super().save(*args, **kwargs)