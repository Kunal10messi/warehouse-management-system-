from django.contrib import admin
from django.urls import include, path
from accounts.views import dashboard, root_redirect
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Root controller
    path('', root_redirect, name='root'),

    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Dashboards
    path('dashboard/', dashboard, name='employee_dashboard'),
    path('admin-panel/', include('adminpanel.urls')),

    # Apps
    path('inventory/', include('inventory.urls')),
    path('allocations/', include('allocations.urls')),

    # Django admin
    path('admin/', admin.site.urls),
]