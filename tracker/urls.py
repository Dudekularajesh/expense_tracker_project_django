from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('' , views.base, name="base"),
    path('login/' , views.login_view , name="login_view"),
    path('register/' , views.register_view , name="register_view"),
    path('logout/' , views.logout_view , name="logout_view"),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('check_availability/', views.check_availability, name='check_availability'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html'
    ), name='password_reset'),

    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'
    ), name='password_reset_complete'),

    path('edit/<int:tx_id>/', views.edit_transaction, name='edit_transaction'),
    path('delete-transaction/<id>/', views.delete_transaction , name="delete_transaction")
]