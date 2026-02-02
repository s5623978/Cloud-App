from django.shortcuts import redirect

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'user' not in request.session:
            return redirect('/')
        return view_func(request, *args, **kwargs)
    return wrapper

