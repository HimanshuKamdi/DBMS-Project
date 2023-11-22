# myapp/views.py
from django.shortcuts import render , redirect
from django.utils import timezone
from .forms import RegistrationForm
from .models import *
from django.contrib import messages
import random 

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

            voter_id = new_voter.Voter_ID ; 
            # Perform any additional actions if needed
            # Redirect or render success page
            #return render(request, 'registration_success.html')
            return redirect(f'/register/details/{voter_id}')
        else:
            print("Form is invalid")
            print(form.errors)
    else:
        print("Received GET request")
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def details(request , voter_id):

    if request.method== "POST":
        First_Name = request.POST.get('First_Name')
        Last_Name =request.POST.get('Last_Name')
        Contact_Number = request.POST.get('Contact_Number')
        Address = request.POST.get('Address')
        Date_of_Birth = request.POST.get('DOB')
        city = request.POST.get('city')
        print(city) 
        temp = Constituencies.objects.get(City = city)
        c_id = temp.Constituency_ID  
        new_voter_details = Voter_Details.objects.create(
                Voter_ID = voter_id , 
                First_Name=First_Name,
                Last_Name=Last_Name,
                Contact_Number = Contact_Number ,
                Address = Address ,
                Date_of_Birth = Date_of_Birth ,
                Constituency_ID = c_id ,
                Voter_Card_Number = random.randint(1000000000, 9999999999)

                # Verified_By=None
            )
        new_voter_details.save() 

        return redirect('/login/') 
        
            
        
    return render(request , 'details.html') 



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



def login_page_admin(request):
    if request.method== "POST":
        Username = request.POST.get('Username')
        Password =request.POST.get('Password')

        if not Admins.objects.filter(Username =Username).exists():
            messages.error(request ,"Username doesn't exist")
            print("Username not exits")
            return redirect('/login/')
        
        admin = Admins.authenticate_voter(Username, Password) 
        if admin is None :  
            messages.error(request , "Invalid credentials")
            return redirect('/register/')
        
 
        else:
            print("Hello") ; 
            return redirect('/admin_home.html/')
            
        
    return render(request , 'login.html') 
