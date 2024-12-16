# Generated by Django 5.1.4 on 2024-12-16 15:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("faunatrack", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="GPS",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("latitude", models.DecimalField(decimal_places=5, max_digits=8)),
                ("longitude", models.DecimalField(decimal_places=5, max_digits=8)),
            ],
        ),
        migrations.AddField(
            model_name="espece",
            name="status",
            field=models.CharField(
                choices=[
                    ("DANGER", "En voie de disparition"),
                    ("OK", "Espèce non menacé"),
                ],
                default="OK",
                max_length=255,
                verbose_name="status de l'espèce",
            ),
        ),
        migrations.AlterField(
            model_name="espece",
            name="nom",
            field=models.CharField(
                default="", max_length=255, verbose_name="Nom de l'espèce"
            ),
        ),
        migrations.CreateModel(
            name="ProfilScientifique",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profil_scientifique",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Projet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "titre",
                    models.CharField(
                        default="Projet sans titre",
                        max_length=255,
                        verbose_name="Titre du projet",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        default=None,
                        null=True,
                        verbose_name="Description du projet",
                    ),
                ),
                ("date_creation", models.DateField(auto_now_add=True)),
                ("date_maj", models.DateTimeField(auto_now=True)),
                (
                    "scientifiques",
                    models.ManyToManyField(
                        related_name="projets", to="faunatrack.profilscientifique"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Observation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantite", models.IntegerField(default=0)),
                ("date_observation", models.DateTimeField()),
                (
                    "notes",
                    models.TextField(default="Pas de notes pour cette observation"),
                ),
                (
                    "photo",
                    models.ImageField(
                        blank=True,
                        default=None,
                        null=True,
                        upload_to="faunatrack/static/photo_observations",
                    ),
                ),
                (
                    "emplacement",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="observations",
                        to="faunatrack.gps",
                    ),
                ),
                (
                    "espece",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="observations",
                        to="faunatrack.espece",
                    ),
                ),
                (
                    "scientifique",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="observations",
                        to="faunatrack.profilscientifique",
                    ),
                ),
                (
                    "projet",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="observations",
                        to="faunatrack.projet",
                    ),
                ),
            ],
        ),
    ]