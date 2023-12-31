# myapp/views.py
from django.shortcuts import render , redirect
from django.utils import timezone
from .forms import RegistrationForm
from .models import *
from django.contrib import messages
import random 
from datetime import datetime 

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
        # Date_of_Birth = datetime.strptime(Date_of_Birth, '%Y-%m-%d').date()
        
        city = request.POST.get('city')
        temp = Constituencies.objects.get(City = city)  
        temp_ID = Voters.objects.get(Voter_ID =  voter_id)
        new_voter_details = Voter_Details.objects.create(
                Voter_ID = temp_ID , 
                First_Name=First_Name,
                Last_Name=Last_Name,
                Contact_Number = Contact_Number ,
                Address = Address ,
                Date_of_Birth = Date_of_Birth ,
                Constituency_ID = temp ,
                Voter_Card_Number = random.randint(1000000000, 9999999999)

            )
        new_voter_details.save() 

        return redirect('/') 
        

    return render(request , 'details.html') 



def login_page(request):
    if request.method== "POST":
        Username = request.POST.get('Username')
        Password =request.POST.get('Password')

        if not Voters.objects.filter(Username =Username).exists():
            messages.error(request ,"Username doesn't exist")
            print("Username not exits")
            return redirect('/')
        
        user = Voters.authenticate_voter(Username, Password) 
        if user is None :
            messages.error(request , "Invalid credentials")
            return redirect('/')
        
 
        else:
            print("Hello") ; 
            return redirect(f'/home/{user.Voter_ID}')
            
        
    return render(request , 'login.html') 

def admin_page(request):
    supervisors = Supervisor.objects.select_related('Admin_ID', 'Constituency_ID').all()

    list_of_supervisors = []

    for supervisor in supervisors:
        supervisor_id = supervisor.Admin_ID.Admin_ID  
        supervisor_name = supervisor.Admin_ID.First_Name + ' ' + supervisor.Admin_ID.Last_Name
        constituency_name = supervisor.Constituency_ID.Constituency_Name 
        list_of_supervisors.append((supervisor_id,supervisor_name, constituency_name))
    #temp = Voters.objects.filter(Verified = "No")
    #c_id = []
    #for voter in temp:
        #c_id.append(voter.Voter_ID) 

    #voters = Voter_Details.objects.filter(Voters.Voter_ID  in c_id)
    voters = Voter_Details.objects.all()
    voters_list = []
    # constituency_name = Voter_Details.objects.select_related('Constituency_ID').all()
    for voter in voters:
        voter_id = voter.Voter_Card_Number
        voter_detail = Voters.objects.get(Voter_ID = voter.Voter_ID.Voter_ID)
        voter_verified = voter_detail.Verified
        voter_firstname = voter.First_Name
        voter_lasttname = voter.Last_Name
        voter_dob = voter.Date_of_Birth
        voter_contact = voter.Contact_Number
        voter_voter_number = voter.Voter_Card_Number
        try:
            constituency_name = voter.Constituency_ID.Constituency_Name
        except:
            pass
        details = {
            "First_Name":voter_firstname,
            "Last_Name":voter_lasttname,
            "Date_of_Birth":voter_dob,
            "Contact_Number":voter_contact,
            "Voter_Card_Number":voter_voter_number,
            "Constituency_Name":constituency_name,
            "Verified":voter_verified            
        }
        voters_list.append(details)        

    candidates = Candidates.objects.all()
    candidates_list = []
    for candidate in candidates:
        id = candidate.Candidate_ID 
        name = candidate.Candidate_Name
        party_id = candidate.Party_ID
        try:
            party = Parties.objects.get(Party_ID = party_id.Party_ID)
            party_name = party.Party_Name
        except:
            party_name= "NULL"
        constituency= Constituencies.objects.get(Constituency_ID = candidate.Constituency_ID.Constituency_ID)
        constituency_name= constituency.Constituency_Name 
        election_year = candidate.Election_Year
        description = candidate.Candidate_Description
        details= {
            "id": id ,
            "name": name,
            "party_name": party_name,
            "constituency_name": constituency_name,
            "election_year": election_year,
            "description": description
        }

        candidates_list.append(details)


    context = {'list_of_supervisors': list_of_supervisors, 'voters_list': voters_list, 'candidates_list': candidates_list}  
    return render(request,'admin.html',context)


def login_page_admin(request):
    if request.method== "POST":
        Username = request.POST.get('Username')
        Password =request.POST.get('Password')

        if not Admins.objects.filter(Username =Username).exists():
            messages.error(request ,"Username doesn't exist")
            print("Username not exits")
            return redirect('/login/')
        
        admin = Admins.authenticate_admin(Username, Password) 
        if admin is None :  
            messages.error(request , "Invalid credentials")
            return redirect('/admin_login')
        
 
        else:
            print("Hello") ; 
            return redirect('/admin')
            
        
    return render(request , 'admin_login.html') 

def profile_page(request,id):
    details = Voter_Details.objects.filter(Voter_ID = id)    
    return render(request,'profile.html',details )


def delete_supervisor(request , supervisor_id):
    print(supervisor_id)     
    temp = Supervisor.objects.get(Admin_ID = supervisor_id) 
    temp.delete()

    return redirect('/admin')


def approve_voter(request , voter_id):
    temp = Voter_Details.objects.get(Voter_Card_Number = voter_id)
    temp = Voters.objects.get(Voter_ID = temp.Voter_ID.Voter_ID)
    temp.Verified = "Yes" 
    temp.save() 

    return redirect('/admin/')

def reject_voter(request , voter_id):
    temp = Voter_Details.objects.get(Voter_Card_Number = voter_id)
    number = temp.Voter_ID 
    temp = Voters.objects.get(Voter_ID = number.Voter_ID)
    temp.delete()

    return redirect('/admin/')


def home(request, voter_id):
    voter_details = Voter_Details.objects.get(Voter_ID=voter_id)
    more_details = Voters.objects.get(Voter_ID=voter_id)
    try:
        constituency_id=Constituencies.objects.get(Constituency_ID= voter_details.Constituency_ID.Constituency_ID)
    except:
        constituency_id= "NULL"
    try:
        candidates = Candidates.objects.filter(Constituency_ID=constituency_id.Constituency_ID)
    except:
        candidates = []
    candidates_list = []
    for candidate in candidates:
        name = candidate.Candidate_Name
        party_id = candidate.Party_ID
        try:
            party = Parties.objects.get(Party_ID = party_id.Party_ID)
            party_name = party.Party_Name
        except:
            party_name= "NULL"
        constituency_name= candidate
        election_year = candidate.Election_Year
        description = candidate.Candidate_Description
        details= {
            "name": name,
            "party_name": party_name,
            "constituency_name": constituency_name,
            "election_year": election_year,
            "description": description
        }

        candidates_list.append(details)
    context={"details":voter_details, "more_details":more_details, "candidates":candidates_list}
    return render(request , 'home.html' , context = context)

def add_supervisor(request):
    if request.method== "POST":
        username  = request.POST.get('Username')
        password = request.POST.get('Password')
        first_name = request.POST.get('First_Name')
        last_name =request.POST.get('Last_Name')
        email =request.POST.get('Email')
        constituency = request.POST.get('Constituency')
        new_supervisor_details = Admins.objects.create(
                Username = username,
                Password = password,
                First_Name = first_name,
                Last_Name = last_name,
                Email = email,
                Role = 'Supervisor'
            )
        new_supervisor_details.save() 
        constituency_detail = Constituencies.objects.get(City = constituency) 
        supervisor = Admins.objects.get(Email = email)
        new_entry = Supervisor.objects.create(
            Constituency_ID = constituency_detail,
            Admin_ID = supervisor

        )
        new_entry.save()


        return redirect('/admin')
    return render(request,'add_supervisor.html')

def add_candidate(request):
    if request.method== "POST":
        name  = request.POST.get('Name')
        party_name =request.POST.get('Party_Name')
        constituency = request.POST.get('Constituency')
        year = request.POST.get('Year')
        description = request.POST.get('Description')
        party=Parties.objects.get(Party_Name = party_name)
        constituency_detail = Constituencies.objects.get(City = constituency) 
        new_candidate_details = Candidates.objects.create(
                Candidate_Name = name,
                Party_ID = party,
                Constituency_ID = constituency_detail,
                Election_Year = year,
                Candidate_Description = description
            )
        new_candidate_details.save() 
        return redirect('/admin')
    return render(request,'add_candidate.html')


def reject_candidate(request , voter_id):
    temp =  Candidates.objects.get(Candidate_ID = voter_id)
    temp.delete()

    return redirect('/admin/')


def reject_supervisor(request , voter_id):
    temp = Supervisor.objects.get(Admin_ID = voter_id) 
    temp.delete()

    return redirect('/admin')