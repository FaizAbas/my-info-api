from django.urls import path

from . import views

urlpatterns = [
    path('', views.my_info_view, name='callback'),
    path('start', views.my_info_start_view, name='start')
]
