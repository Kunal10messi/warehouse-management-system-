from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def employee_dashboard(request):
    return render(request, 'employee/dashboard.html')


@login_required
def dashboard(request):
    if request.user.role == 'ADMIN':
        return redirect('/admin-panel/')
    else:
        return render(request, 'employee/dashboard.html')
    
def root_redirect(request):
    if request.user.is_authenticated:
        if request.user.role == 'ADMIN':
            return redirect('admin_dashboard')
        return redirect('employee_dashboard')
    return redirect('login')