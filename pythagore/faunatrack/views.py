
from django.shortcuts import render, redirect
from django.contrib import messages


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