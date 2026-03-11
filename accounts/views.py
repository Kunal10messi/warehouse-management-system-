from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from datetime import date
from allocations.models import Assignment


@login_required
def employee_dashboard(request):

    today = date.today()

    assignments = Assignment.objects.filter(
        user=request.user,
        actual_return_date__isnull=True
    ).select_related("device")

    notifications = []

    for a in assignments:

        device_name = f"{a.device.device_type} ({a.device.serial_number})"
        days_left = (a.expected_return_date - today).days

        # Show if overdue OR due within 3 days
        if days_left <= 3:

            if days_left < 0:
                notifications.append(
                    f"⛔ {device_name} is overdue by {abs(days_left)} day(s)"
                )

            elif days_left == 0:
                notifications.append(
                    f"🔔 {device_name} must be returned today"
                )

            elif days_left == 1:
                notifications.append(
                    f"⚠ {device_name} must be returned tomorrow"
                )

            else:
                notifications.append(
                    f"⚠ {device_name} must be returned in {days_left} day(s)"
                )

    return render(request, 'employee/dashboard.html', {
        "notifications": notifications
    })


@login_required
def dashboard(request):
    if request.user.role == 'ADMIN':
        return redirect('/admin-panel/')
    else:
        return employee_dashboard(request)


def root_redirect(request):
    if request.user.is_authenticated:
        if request.user.role == 'ADMIN':
            return redirect('admin_dashboard')
        return redirect('employee_dashboard')
    return redirect('login')