
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User

from faunatrack.models import ProfilScientifique

# Don't forget to register the signals in the apps.py !!

@receiver(post_save, sender=User)
def add_scientifique_to_user(sender, instance, created, **kwargs):
    if created:
        ProfilScientifique.objects.create(
            user=instance,
            domaine_de_recherche="Chercheur en biodiversité"
        )
