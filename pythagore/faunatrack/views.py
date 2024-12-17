
from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from faunatrack.models import Observation, Projet
from faunatrack.forms import ObservationForm


class ObservationList(ListView):
    model = Observation
    template_name = "observations/list.html"


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

class ObservationDelete(DeleteView):
    model = Observation
    template_name = "observations/confirm_delete.html"
    success_url = reverse_lazy('observation_list')

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
    return render(request, "faunatrack_accueil.html")


                      