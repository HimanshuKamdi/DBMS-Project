from django.urls import path
from voters.views import * 

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_page, name='login'),
    path('admin/', admin_page, name='admin'),
]