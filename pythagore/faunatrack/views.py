
import datetime
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
    permission_required = "faunatrack.change_observation" # Don't forget the app name before the permissions !
    # "faunatrack.view_observation", "faunatrack.delete_observation", "faunatrack.add_observation" 


class ObservationCreate(CreateView):
    model = Observation
    template_name = "observations/form.html"
    form_class = ObservationForm
    success_url = reverse_lazy('observation_list')

    # Correct implementation of form_valid
    def form_valid(self, form):
        if form.cleaned_data.get("quantite") < 5:
            form.add_error("quantite","Quantité ne peut être inférieur à 5")
            return self.form_invalid(form)

        return super().form_valid(form)
    
class ObservationUpdate(UpdateView):
    model = Observation
    template_name = "observations/form.html"
    form_class = ObservationForm
    success_url = reverse_lazy('observation_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['gandalf'] = 'Un magicien n est jamais en retard'
        return data
    
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


                      