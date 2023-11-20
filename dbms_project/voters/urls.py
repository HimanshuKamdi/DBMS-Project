from django.urls import path
from voters.views import register

urlpatterns = [
    path('register/', register, name='register'),
    # path('login/', login, name='login'),
]