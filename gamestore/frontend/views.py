import email
from django.shortcuts import redirect, render
from .firebase import db
from django.contrib import messages
from firebase_admin import auth
from .auth import login_user, create_user
from .auth import logout
from .decorators import login_required


def landing(request):
    if 'user' in request.session:
        return redirect('/store/')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        action = request.POST.get('action')

        # logging in!
        if action == 'login':

            try:
                result = login_user(email, password)
            except Exception as e:
                messages.error(request, f"Could not log in: {e}")
                return render(request, 'frontend/landing.html')

            if not result:
                messages.error(request, "Invalid email or password")
                return render(request, 'frontend/landing.html')

            decoded = auth.verify_id_token(result["idToken"])

            request.session['user'] = {
                "uid": decoded["uid"],
                "email": decoded["email"]
            }
            request.session.set_expiry(0)

            return redirect('/store/')

        # signing up!
        elif action == 'signup':

            try:
                result = create_user(email, password)
            except Exception as e:
                messages.error(request, f"Could not create account: {e}")
                return render(request, 'frontend/landing.html')

            messages.success(request, "Account created! You can now log in.")
            return render(request, 'frontend/landing.html')

    return render(request, 'frontend/landing.html')

@login_required
def store(request):
    games_ref = db.collection("games").stream()

    games = []
    for game in games_ref:
        games.append(game.to_dict())

    if request.method == 'POST':
        action = request.POST.get('action')

        # logging out!
        if action == 'logout':
            logout(request)
            return redirect('/')

    return render(request, "frontend/store.html", {"games": games})

@login_required
def checkout(request):
    return render(request, 'frontend/checkout.html')
