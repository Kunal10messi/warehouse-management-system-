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