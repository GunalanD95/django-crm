from django.urls import path
from django.urls.conf import include
from . import views


urlpatterns = [
    path('',views.index, name='login'),
    path('logout/',views.logout_view, name='logout'),
]