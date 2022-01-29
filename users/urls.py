from django.urls import path
from django.urls.conf import include
from . import views


urlpatterns = [
    path('login/',views.index, name='login'),
    path('logout/',views.logout_view, name='logout'),
    path('contact/',views.contact, name='contact'),
    path('account/',views.account, name='account'),
    path('reset_password/',views.reset_password, name='reset_password'),
    path('reset_mail/',views.reset_mail, name='reset_mail'),
    path('mail_sent',views.mail_sent, name='mail_sent'),

]