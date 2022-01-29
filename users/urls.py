from django.urls import path
from django.urls.conf import include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/',views.index, name='login'),
    path('logout/',views.logout_view, name='logout'),
    path('contact/',views.contact, name='contact'),
    path('account/',views.account, name='account'),
    # path('reset_password/',views.reset_password, name='reset_password'),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='users/mail_sent.html'),name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='users/reset_mail.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='users/reset.html'),name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('reset_mail/',views.reset_mail, name='reset_mail'),
    path('mail_sent',views.mail_sent, name='mail_sent'),

]