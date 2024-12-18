from django.contrib import admin
from faunatrack.models import Espece, Observation, ProfilScientifique, Projet, GPS
from import_export.admin import ImportExportModelAdmin, ImportExportMixin

from import_export import resources, fields
from django.core.mail import send_mail



class EspeceResource(resources.ModelResource):
    nom = fields.Field(attribute="nom", column_name="nom_espece")

    class Meta:
        model = Espece 
        # fields = ["nom", 'status']
        # skip_unchanged = True # Ignorer les modifications lors de l'import si une ligne existe déjà
        # report_skipped = False  # Ignorer les modifications dans le rapport généré



# Register your models here.
@admin.register(Espece)
class EspeceAdmin(ImportExportModelAdmin):
    list_display = ["nom", "status"]
    list_editable = ["status"]
    list_filter = ["status"]
    search_fields = ["nom"]
    ordering = ["status"]

    actions = ["marquer comme en danger"]

    def get_import_resource_class(self, request):
        return EspeceResource
    
    def get_export_resource_class(self, request):
        return EspeceResource

@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = ["get_gps", "espece__nom", "scientifique__user__username"]
    ordering = ["-date_observation"]
    actions = ["projet_critique"]

    def get_gps(self, object: Observation):
        return f'{object.emplacement.latitude}, {object.emplacement.longitude}'
    
    get_gps.short_description = "Emplacement"

    def projet_critique(self, request, queryset):
        print(Observation.objects.all()) # Queryset
        for observation in queryset:
            projet = observation.projet
            projet.description = "[CRITIQUE] " + projet.description
            projet.save()
        self.message_user(request, "Le projet a été marqué comme critique")  
        send_mail(
            "Un projet a été marqué comme critique",
            "Un projet a été marqué comme critique.",
            "from@example.com",
            ["to@example.com"],
            fail_silently=False,
        ) 

        #         # First, render the plain text content.
        # text_content = render_to_string(
        #     "templates/emails/my_email.txt",
        #     context={"my_variable": 42},
        # )

        # # Secondly, render the HTML content.
        # html_content = render_to_string(
        #     "templates/emails/my_email.html",
        #     context={"my_variable": 42},
        # )

        # # Then, create a multipart email instance.
        # msg = EmailMultiAlternatives(
        #     "Subject here",
        #     text_content,
        #     "from@example.com",
        #     ["to@example.com"],
        #     headers={"List-Unsubscribe": "<mailto:unsub@example.com>"},
        # )

        # # Lastly, attach the HTML content to the email instance and send.
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()
    projet_critique.short_description = "Marquer le projet comme étant critique"    



@admin.register(ProfilScientifique)
class ProfilScientifiqueAdmin(admin.ModelAdmin):
    list_display = ["id"]


class ObservationInlineAdmin(admin.TabularInline):
    model = Observation


@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ["id"]
    inlines = [ObservationInlineAdmin]

@admin.register(GPS)
class GPSAdmin(admin.ModelAdmin):
    list_display = ["id"]