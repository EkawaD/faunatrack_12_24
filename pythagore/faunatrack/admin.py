from django.contrib import admin
from faunatrack.models import Espece, Observation, ProfilScientifique, Projet, GPS

# Register your models here.
@admin.register(Espece)
class EspeceAdmin(admin.ModelAdmin):
    list_display = ["nom", "status"]
    list_editable = ["status"]
    list_filter = ["status"]
    search_fields = ["nom"]
    ordering = ["status"]

    actions = ["marquer comme en danger"]

@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = ["get_gps", "espece__nom", "scientifique__user__username"]
    ordering = ["-date_observation"]

    def get_gps(self, object: Observation):
        return f'{object.emplacement.latitude}, {object.emplacement.longitude}'
    
    get_gps.short_description = "Emplacement"


@admin.register(ProfilScientifique)
class ProfilScientifiqueAdmin(admin.ModelAdmin):
    list_display = ["id"]


@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ["id"]

@admin.register(GPS)
class GPSAdmin(admin.ModelAdmin):
    list_display = ["id"]