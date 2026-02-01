import email
from django.shortcuts import redirect, render
from .firebase import db
from django.contrib import messages
from firebase_admin import auth
from .auth import login_user, create_user
from .auth import logout
from .decorators import login_required
from datetime import datetime


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
    i = 0
    for game in games_ref:
        games.append(game.to_dict())
        games[i].update({"id": game.id})
        i += 1

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_to_basket':
            basket = request.session.get('basket', {})

            game_id = request.POST.get('game_id')
            title = request.POST.get('title')
            price = float(request.POST.get('price'))
            print("Adding game to basket:", game_id)

            if game_id in basket:
                basket[game_id]['qty'] += 1
            else:
                basket[game_id] = {
                    'title': title,
                    'price': price,
                    'qty': 1
                }

            request.session['basket'] = basket
            messages.success(request, f"{title} added to basket!")

        # logging out!
        elif action == 'logout':
            logout(request)
            return redirect('/')

    return render(request, "frontend/store.html", {"games": games})

@login_required
def checkout(request):
    basket = request.session.get('basket', {})

    total = sum(
        item['price'] * item['qty']
        for item in basket.values()
    )

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'remove_from_basket':
            game_id = request.POST.get('game_id')
            print("Removing game:", game_id)
            print("Current basket before removal:", basket)

            if game_id in basket:
                if basket[game_id]['qty'] > 1:
                    basket[game_id]['qty'] -= 1
                else:
                    del basket[game_id]

            request.session['basket'] = basket

            print("Updated basket after removal:", basket)

            return redirect('/checkout/')

        elif action == 'place_order':
            basket = request.session.get('basket', {})

            if not basket:
                messages.error(request, "Your basket is empty.")
                return redirect('/checkout/')

            user = request.session['user']

            items = []
            total = 0

            for item in basket.values():
                items.append({
                    "title": item['title'],
                    "price": item['price'],
                    "qty": item['qty']
                })
                total += item['price'] * item['qty']

            db.collection("orders").add({
                "user_id": user['uid'],
                "email": user['email'],
                "items": items,
                "total": total,
                "timestamp": datetime.now()
            })

            # clear basket
            request.session['basket'] = {}

            messages.success(request, "Order placed successfully! Thank you!")
        
        # logging out!
        elif action == 'logout':
            logout(request)
            return redirect('/')

    return render(request, 'frontend/checkout.html', {'basket': basket, 'total': total})
