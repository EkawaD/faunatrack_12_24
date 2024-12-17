
from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from faunatrack.models import Espece, Observation, ProfilScientifique, Projet
from faunatrack.forms import ObservationForm

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin

class AuthorizationMixin(LoginRequiredMixin, PermissionRequiredMixin):
    pass

class ObservationList(AuthorizationMixin, ListView):
    model = Observation
    template_name = "observations/list.html"
    permission_required = "change_observation" #, "change_observation", "delete_observation", "add_observation" ~ Dont work


class ObservationCreate(CreateView):
    model = Observation
    template_name = "observations/form.html"
    form_class = ObservationForm
    success_url = reverse_lazy('observation_list')

    # def form_valid(self, form):
    #     if form.cleaned_data['quantite'] < 5:
    #         raise ValidationError("Rien observé ?")

    #     return super().form_valid(form)
    
class ObservationUpdate(UpdateView):
    model = Observation
    template_name = "observations/form.html"
    form_class = ObservationForm
    success_url = reverse_lazy('observation_list')

    def get_context_data(self, context):
        context["gandalf"] = "Un magicien n'est jamais en retard"
        return context

class ObservationDelete(UserPassesTestMixin, DeleteView):
    model = Observation
    template_name = "observations/confirm_delete.html"
    success_url = reverse_lazy('observation_list')

    def test_func(self):
        try:
            return self.request.user.profil_scientifique
        except ProfilScientifique.DoesNotExist:
            messages.error(self.request, "Vous n'êtes pas scientifique !", extra_tags="text-red-500")
            return False
        
        # if not self.request.user.profil_scientifique: 
        #     return False
        # return True

class ObservationDetail(DetailView):
    model = Observation
    template_name = "observations/detail.html"

class ProjetList(ListView):
    model = Projet
    template_name = "projets/list.html"


def observation_list(request):
    observations = Observation.objects.all()
    return render(request, 'observations/list.html', {
        "object_list": observations
    })

def bonjour(request):
    messages.add_message(request, messages.INFO, "Bienvenue !")
    return render(request, 'home.html', {
        "couleur_du_ciel": "bleu"
    })

import datetime
# https://refactoring.guru
# https://refactoring.guru/fr/replace-nested-conditional-with-guard-clauses
def faunatrack_home(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('home')



    data = Observation.objects.all().filter(espece__nom__startswith="O").exclude(date_observation__gt=datetime.date.today())
    try:
        espece = Espece.objects.get(id=50) # Lève une exception DoestNotExists !!
    except Espece.DoesNotExist:
        espece = None

    espece = Espece.objects.filter(id=50)
    observations = Observation.objects.select_related("emplacement").all() # Récupère les ids de "emplacement" AVANT la requpete SQL, pratique si une ligne de la db est requếté plusieurs fois
    return render(request, "faunatrack_accueil.html", {
        "data": data
    })


                      