from django.urls import path
from . import views

urlpatterns = [
    path('register/add_user/',views.add_user,name='add_user'),
    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),
    path('dashboard/ia/save_parameters/', views.save_parameters, name='save_parameters'),
    path('dashboard/payment/hours/',views.update_hours,name='update_hours'),
    path('dashboard/ia/upload_csv/', views.upload_csv, name='upload_csv'),
    path('emailRetrieve/recoverPassword/',views.recover_password_email,name='recover_password_email'),
    path('recover_password/<str:token>/',views.recover_password,name='recover_password'),
    path('delete_model/<str:model_id>/<str:dataset_id>/',views.delete_model,name='delete_model'),
    path('dashboard/account/update/',views.update_profile,name='update_profile'),
]
