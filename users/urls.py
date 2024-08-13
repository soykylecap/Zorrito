from django.urls import path
from django.contrib import admin
from users import views
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [
    path('login/', views.login_request, name="Login"),
    path('register/', views.register, name="Register"),
    path('edit/', views.edit, name="Edit"),
    path('logout/', views.UsersLogoutView.as_view(template_name='AppZorro/index.html'), name="LogoutZorro"),
]


urlpatterns += [
    path('password_reset/', PasswordResetView.as_view(template_name='users/password_reset_form.html'), name='PasswordReset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]
