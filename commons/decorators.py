from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect
from django.views import View


def redirect_to_home_if_authenticated(func):
    def inner_func(*args, **kwargs):
        if args and args[0]:
            if isinstance(args[0], View):
                request = args[0].request
            elif isinstance(args[0], WSGIRequest):
                request = args[0]
            else:
                return func(*args, **kwargs)
            if request.user.is_authenticated:
                return redirect('home')
        return func(*args, **kwargs)
    return inner_func
