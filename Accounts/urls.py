from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path('doctors/', views.doctors_list, name='doctors_list'),
    path('detail/<int:doctor_id>/', views.doctor_details, name='detail_page'),
    path('booking/<int:doctor_id>/',
         views.doctor_reservation, name='doctor_reservation'),



    path('patient/edit/', views.edit_pateint_profile, name='patient_edit'),



    path('', views.home_redirect, name='home_redirect'),


    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),


    path('register/', views.register, name='register'),


    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),


    path('change-password/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/change_password.html',
        success_url='/accounts/change-password/done/'
    ), name='change_password'),

    path('change-password/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/change_password_done.html'
    ), name='password_change_done'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html'
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),

]
