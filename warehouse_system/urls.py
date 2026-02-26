from django.contrib import admin
from django.urls import include, path
from accounts.views import dashboard

from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard),
]

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard),
    path('inventory/', include('inventory.urls')),
    path('allocations/', include('allocations.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin-panel/', include('adminpanel.urls')),
]

