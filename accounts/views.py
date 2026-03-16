from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from datetime import date, timedelta
from allocations.models import Assignment, DeviceRequest


@login_required
def employee_dashboard(request):
    today = date.today()
    two_days_ago = today - timedelta(days=2)

    notifications = []

    #approval
    recent_approvals = Assignment.objects.filter(
        user=request.user,
        approval_seen=False,
        issue_date__gte=two_days_ago
    ).select_related('device')

    for a in recent_approvals:
        notifications.append({
            'message': f"✅ {a.device.device_type} ({a.device.serial_number}) was assigned to you on {a.issue_date}. Expected return: {a.expected_return_date}.",
            'type': 'approval'
        })
    recent_approvals.update(approval_seen=True)

    #rejection 
    recent_rejections = DeviceRequest.objects.filter(
        user=request.user,
        status='REJECTED',
        rejection_seen=False,
        request_date__date__gte=two_days_ago
    ).select_related('device')

    for r in recent_rejections:
        notifications.append({
            'message': f"❌ Your request for {r.device.device_type} ({r.device.serial_number}) could not be fulfilled. Please try another device.",
            'type': 'rejection'
        })
    recent_rejections.update(rejection_seen=True)

    #deadline reminders
    assignments = Assignment.objects.filter(
        user=request.user,
        actual_return_date__isnull=True
    ).select_related('device')

    for a in assignments:
        device_name = f"{a.device.device_type} ({a.device.serial_number})"
        days_left = (a.expected_return_date - today).days

        if days_left <= 3:
            if days_left < 0:
                notifications.append({
                    'message': f"⛔ {device_name} is overdue by {abs(days_left)} day(s). Fine RS-50 per day on late return.",
                    'type': 'overdue'
                })
            elif days_left == 0:
                notifications.append({
                    'message': f"🔔 {device_name} must be returned today. Fine RS-50 per day on late return",
                    'type': 'due_today'
                })
            elif days_left == 1:
                notifications.append({
                    'message': f"⚠ {device_name} must be returned tomorrow. Fine RS-50 per day on late return",
                    'type': 'due_soon'
                })
            else:
                notifications.append({
                    'message': f"⚠ {device_name} must be returned in {days_left} day(s). Fine RS-50 per day on late return.",
                    'type': 'due_soon'
                })

    return render(request, 'employee/dashboard.html', {
        'notifications': notifications
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