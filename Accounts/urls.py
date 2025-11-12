from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    
    path('doctors/', views.doctors_list, name='doctors_list'),
    path('booking/<int:doctor_id>/', views.booking_page, name='booking_page'),
    
    path('login/', auth_views.LoginView.as_view(template_name='accounts/templates/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    


    path('change-password/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/templates/change_password.html',
        success_url='/accounts/templates/change-password/done/'
    ), name='change_password'),

    path('change-password/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/templates/change_password_done.html'
    ), name='password_change_done'),

    


    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/templates/password_reset.html'
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/templates/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/templates/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/templates/password_reset_complete.html'
    ), name='password_reset_complete'),
]
