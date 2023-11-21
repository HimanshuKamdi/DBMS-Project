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
