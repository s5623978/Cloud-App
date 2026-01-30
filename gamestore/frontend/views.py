from django.shortcuts import render
from .firebase import db

def landing(request):
    return render(request, 'frontend/landing.html')

def store(request):
    games_ref = db.collection("games").stream()

    games = []
    for game in games_ref:
        games.append(game.to_dict())

    return render(request, "frontend/store.html", {"games": games})

def checkout(request):
    return render(request, 'frontend/checkout.html')
