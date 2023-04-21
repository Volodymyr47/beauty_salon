from django.shortcuts import render


def salon_admin_required(func):
    def wrapper(*args, **kwargs):
        if not args[0].user.groups.filter(name='salon_admin').exists():
            return render(args[0], 'salon_admin/404.html', status=404)
        return func(*args, **kwargs)
    return wrapper


def simple_user_required(func):
    def wrapper(*args, **kwargs):
        if args[0].user.groups.filter(name='salon_admin').exists():
            return render(args[0], 'salon/404.html', status=404)
        return func(*args, **kwargs)
    return wrapper
