# myapp/views.py
from django.shortcuts import render , redirect
from django.utils import timezone
from .forms import RegistrationForm
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login

def register(request):
    print("Received request")
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print("Received POST request")
        if form.is_valid():
            print("Form is valid")
            email = form.cleaned_data['Email']
            username = form.cleaned_data['Username']
            password = form.cleaned_data['Password']
            print("Saved form")
            # Save to Voters table
            new_voter = Voters.objects.create(
                Username=username,
                Password=password,
                Email=email,
                Registration_Date=timezone.now(), 
                Last_Login=timezone.now(),
                Verified='No'
                # Verified_By=None
            )
            new_voter.save()
            print("Created new user")
            # Perform any additional actions if needed
            # Redirect or render success page
            #return render(request, 'registration_success.html')
            return redirect('/register')
        else:
            print("Form is invalid")
            print(form.errors)
    else:
        print("Received GET request")
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def login_page(request):
    if request.method== "POST":
        Username = request.POST.get('Username')
        Password =request.POST.get('Password')

        if not Voters.objects.filter(Username =Username).exists():
            messages.error(request ,"Username doesn't exist")
            print("Username not exits")
            return redirect('/login/')
        
        user = Voters.authenticate_voter(Username, Password)
        if user is None :
            messages.error(request , "Invalid credentials")
            return redirect('/register/')
        
 
        else:
            print("Hello") ; 
            return redirect('/home.html/')
            
        
    return render(request , 'login.html') 

def admin_page(request):
    supervisors = Supervisor.objects.select_related('Admin_ID', 'Constituency_ID').all()

    list_of_supervisors = []

    for supervisor in supervisors:
        supervisor_name = supervisor.Admin_ID.First_Name + ' ' + supervisor.Admin_ID.Last_Name
        constituency_name = supervisor.Constituency_ID.Constituency_Name 
        list_of_supervisors.append((supervisor_name, constituency_name))

    voters = Voter_Details.objects.all()
    voters_list = []
    # constituency_name = Voter_Details.objects.select_related('Constituency_ID').all()
    for voter in voters:
        voter_firstname = voter.First_Name
        voter_lasttname = voter.Last_Name
        voter_dob = voter.Date_of_Birth
        voter_contact = voter.Contact_Number
        voter_voter_number = voter.Voter_Card_Number
        constituency_name = voter.Constituency_ID.Constituency_Name
        details = {
            "First_Name":voter_firstname,
            "Last_Name":voter_lasttname,
            "Date_of_Birth":voter_dob,
            "Contact_Number":voter_contact,
            "Voter_Card_Number":voter_voter_number,
            "Constituency_Name":constituency_name            
        }
        voters_list.append(details)
    
    context = {'list_of_supervisors': list_of_supervisors, 'voters_list': voters_list}  

    return render(request,'admin.html',context)
