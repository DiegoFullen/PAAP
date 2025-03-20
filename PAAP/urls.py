from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    #path('404/',views.error404_view,name='404'),
    path('401/',views.error401_view,name='401'),
    path('500/',views.error500_view,name='500'),
    path('login/',views.login_view,name='login'),
    path('emailRetrieve/',views.emailRetrieve_view,name='emailRetrieve'),
    path('emailNotification/',views.emailNotification_view,name='emailNotification'),
    path('passwordRetrive/<str:token>/',views.passwordRetrive_view,name='passwordRetrive'),
    path('dashboard/',views.dashboard_view,name='dashboard'),
    path('dashboard/ia/',views.ia_view,name='ia'),
    path('dashboard/resources/',views.resources_view,name='resources'),
    #path('dashboard/manual/',views.manual_view,name='manual'),
    path('dashboard/account/',views.account_view,name='account'),
    path('dashboard/account/edit/',views.accountEdit_view,name='accountEdit'),
    path('dashboard/payment/',views.payment_view,name='payment'),
    path('dashboard/payment/upgrade/',views.paymentUpgrade_view,name='paymentUpgrade'),
    path('dashboard/payment/upgrade/plan/',views.upgrade_plan,name='upgrade_plan'),
    path('pricing/',views.pricing_view,name='pricing'),
    path('register/',views.register_view,name='register'),
    #path('dashboard/account/update/',views.update_profile,name='update_profile'),
    path('exit/',views.exit,name='exit'),
    path('gestion_usuarios/', include('gestion_usuarios.urls')),
]
from django.conf.urls import handler404
handler404 = views.error404_view