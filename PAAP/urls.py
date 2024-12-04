
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/',views.login_view,name='login'),
    path('dashboard/',views.dashboard_view,name='dashboard'),
    path('dashboard/ia/',views.ia_view,name='ia'),
    path('gestion_usuarios/', include('gestion_usuarios.urls')),
]
