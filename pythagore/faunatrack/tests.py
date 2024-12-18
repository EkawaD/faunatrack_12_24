from django.test import TestCase
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from faunatrack.models import GPS, Espece, Observation
from faunatrack.signals import add_scientifique_to_user
from django.utils import timezone
# Create your tests here.

# test unitaires => test qui vont tester une fonction, un comportement, et des cas spécifiques
# test end to end => centré sur l'utilisateur => Ajouter une observation
# test d'intégration => Test utiles au développeur pour connaitre les limites de son code.
class EspeceStatusTest(TestCase):

    def setUp(self):
        post_save.connect(add_scientifique_to_user, sender=User)
        self.lion = Espece.objects.create(nom="Lion")
        self.status_sain = Espece.StatusChoice.EN_FORME
        self.status_danger = Espece.StatusChoice.EN_DANGER

    def tearDown(self):
        post_save.disconnect(add_scientifique_to_user, sender=User)
        return super().tearDown()

    def test_espece_status_default(self):
        self.assertEqual(self.lion.status, self.status_sain)
    
    def test_espece_changement_status(self):
        self.gps = GPS.objects.create(latitude=1.00, longitude=1.00)     
        self.user = User.objects.create(username="bastien")
        Observation.objects.create(
            espece=self.lion,
            scientifique=self.user.profil_scientifique,
            emplacement=self.gps,
            quantite=4,
            date_observation=timezone.now()
        )

        Observation.objects.create(
            espece=self.lion,
            scientifique=self.user.profil_scientifique,
            emplacement=self.gps,
            quantite=5,
            date_observation=timezone.now()
        )

        self.assertEqual(self.lion.status, self.status_danger)

        Observation.objects.create(
            espece=self.lion,
            scientifique=self.user.profil_scientifique,
            emplacement=self.gps,
            quantite=1,
            date_observation=timezone.now()
        )

        self.assertEqual(self.lion.status, self.status_sain)

class OtherTest(TestCase):
    pass