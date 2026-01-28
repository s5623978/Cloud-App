from django.shortcuts import render

def landing(request):
    return render(request, 'frontend/landing.html')

def store(request):
    return render(request, 'frontend/store.html')

def checkout(request):
    return render(request, 'frontend/checkout.html')
