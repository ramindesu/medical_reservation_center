from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import patinet_list
# from .views import request_appointment


urlpatterns = [

    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/users/add/', views.admin_add_user, name='admin_add_user'),
    path('admin/users/<str:user_type>/',
         views.admin_manage_users, name='admin_manage_users'),
    path('admin/users/<int:user_id>/edit/',
         views.admin_edit_user, name='admin_edit_user'),
    path('admin/appointments/', views.admin_manage_appointments,
         name='admin_manage_appointments'),
    path('doctor/appointments/', views.doctor_appointments, name='doctor_appointments'),


    path('doctors/', views.doctors_list, name='doctors_list'),
    path('detail/<int:doctor_id>/', views.doctor_details, name='detail_page'),
    path('booking/<int:doctor_id>/',
         views.doctor_reservation, name='doctor_reservation'),


    path('patient/edit-profile/', views.edit_patient_profile,
         name='edit_patient_profile'),
    path('doctor/edit-profile/', views.edit_doctor_profile,
         name='edit_doctor_profile'),
    path('patient/reservations/', views.full_appointment_history,
         name='full_appointment_history'),
    path(
        'feedback/add/<int:reservation_id>/',
        views.add_feedback,
        name='add_feedback'
    ),
    path("appointment/cancel/<int:appointment_id>/",
         views.cancel_appointment, name="cancel_appointment"),



    path('', views.home_redirect, name='home_redirect'),


    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),


    path('register/', views.register, name='register'),


    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    #     path('edit-profile/', views.edit_doctor_profile, name='edit_doctor_profile'),
    path('edit-profile/', views.edit_patient_profile, name='edit_profile'),
    # path('request-appointment/', views.request_appointment, name='request_appointment'),
    path('appointments/manage/', views.admin_manage_appointments,
         name='manage_appointments'),
    path('appointments/<int:appointment_id>/approve/',
         views.approve_appointment, name='approve_appointment'),
    path('appointments/<int:appointment_id>/reject/',
         views.reject_appointment, name='reject_appointment'),
    path('appointments/<int:appointment_id>/view/',
         views.view_appointment, name='view_appointment'),
    path('appointments/<int:appointment_id>/edit/',
         views.edit_appointment, name='edit_appointment'),

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
    path('doctor/dashboard/patients', patinet_list, name='doctor_patient_list'),




     path('doctor/requests/', views.doctor_requests, name='doctor_requests'),
     path('doctor/requests/<int:reservation_id>/accept/', 
          views.doctor_accept, name='doctor_accept'),
     path('doctor/requests/<int:reservation_id>/reject/', 
          views.doctor_reject, name='doctor_reject'),
     path('doctor/requests/<int:reservation_id>/blacklist/', 
          views.doctor_blacklist, name='doctor_blacklist'),
     path('doctor/requests/<int:reservation_id>/block/', 
         views.doctor_block_request, 
         name='doctor_block_request'),
]
