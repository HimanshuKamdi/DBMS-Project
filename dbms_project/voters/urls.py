from django.urls import path
from voters.views import * 

urlpatterns = [
    path('register/', register, name='register'),
    path('register/details/<int:voter_id>/' , details , name='details') , 
    path('delete/<int:supervisor_id>/' , delete_supervisor , name="delete" ) ,
    path('approve_voter/<int:voter_id' ,approve_voter , name="approve_voter") ,
    path('reject_voter/<int:voter_id>' , reject_voter , name="reject_voter"),  
    path('login', login_page, name='login'),
    path('', login_page, name='login'),
    path('admin/', admin_page, name='admin'),
    path('admin_login', login_page_admin , name = "admin_login"),
    path('profile', profile_page , name = "profile")
]