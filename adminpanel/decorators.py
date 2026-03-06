from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/')
        
        if request.user.role != 'ADMIN':
            return redirect('/')   # send employee back to dashboard
        
        return view_func(request, *args, **kwargs)
    
    return wrapper