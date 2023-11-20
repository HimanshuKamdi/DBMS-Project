# myapp/views.py
from django.shortcuts import render
from django.utils import timezone
from .forms import RegistrationForm
from .models import *
import time

def register(request):
    print("Received request")
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print("Received POST request")
        if form.is_valid():
            print("Form is valid")
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            form.save()
            print("Saved form")
            # Save to Voters table
            new_voter = Voters.objects.create(
                Username=username,
                Password=password,
                Email=email,
                Registration_Date=timezone.now(), 
                Last_Login=timezone.now(),
                Verified='No',
                Verified_By=None
            )
            new_voter.save()
            print("Created new user")
            # Perform any additional actions if needed
            # Redirect or render success page
            return render(request, 'registration_success.html')
        else:
            print("Form is invalid")
    else:
        print("Received GET request")
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})
