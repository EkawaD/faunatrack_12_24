# Generated by Django 5.1.4 on 2024-12-16 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Guitare",
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
                    "marque",
                    models.CharField(
                        default="", max_length=255, verbose_name="marque_guitare"
                    ),
                ),
            ],
        ),
    ]
