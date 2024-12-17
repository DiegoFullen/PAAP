
from django.contrib import admin
from django.urls import path, include
from . import views
from .views import verify_email

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/',views.login_view,name='login'),
    path('dashboard/',views.dashboard_view,name='dashboard'),
    path('dashboard/ia/',views.ia_view,name='ia'),
    path('gestion_usuarios/', include('gestion_usuarios.urls')),
    path('404/',views.error404_view,name='404'),
    path('dashboard/account/',views.account_view,name='account'),
    path('dashboard/account/edit/',views.accountEdit_view,name='accountEdit'),
    path('dashboard/payment/',views.payment_view,name='payment'),
    path('dashboard/payment/upgrade/',views.account_view,name='paymentUpgrade'),
    path('pricing/',views.pricing_view,name='pricing'),
    path('register/',views.register_view,name='register'),
    path('dashboard/account/update/',views.update_profile,name='update_profile'),
    path('register/add_user/',views.add_user,name='add_user'),
    path('gitPAAP/PAAP/',views.exit,name='exit'),
    path('verify-email/<str:token>/', verify_email, name='verify_email'),
]
