from django.urls import path
from voters.views import * 

urlpatterns = [
    path('register/', register, name='register'),
    path('register/details/<int:voter_id>/' , details , name='details') , 
    path('delete/<int:supervisor_id>/' , delete_supervisor , name="delete" ) ,
    path('approve_voter/<int:voter_id>' ,approve_voter , name="approve_voter") ,
    path('reject_voter/<int:voter_id>' , reject_voter , name="reject_voter"),  
    path('login', login_page, name='login'),
    path('home/<int:voter_id>/' , home , name = "home") , 
    path('', login_page, name='login'),
    path('admin/', admin_page, name='admin'),
    path('admin_login', login_page_admin , name = "admin_login"),
    path('profile', profile_page , name = "profile"),
    path('add_supervisor', add_supervisor , name = "add_supervisor"),
    path('add_candidate', add_candidate , name = "add_candidate"),
    path('reject_candidate/<int:voter_id>' , reject_candidate , name= "reject_candidate")
]