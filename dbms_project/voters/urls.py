from django.urls import path
from voters.views import * 

urlpatterns = [
    path('register/', register, name='register'),
    path('register/details/<int:voter_id>/' , details , name='details') , 
    path('login/', login_page, name='login'),
    path('admin/', admin_page, name='admin'),
    path('admin_login', login_page_admin , name = "admin_login"),
    path('profile', profile_page , name = "profile")
]