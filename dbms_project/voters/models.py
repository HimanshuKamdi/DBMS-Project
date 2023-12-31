from django.db import models
from django.contrib.auth.hashers import check_password

class Constituencies(models.Model):
    Constituency_ID = models.AutoField(primary_key=True)
    Constituency_Name = models.CharField(max_length=255)
    City = models.CharField(max_length=255)

    class Meta:
        db_table = 'Constituencies'   



class Parties(models.Model):
    Party_ID = models.AutoField(primary_key=True)
    Party_Name = models.CharField(max_length=255)

    class Meta:
        db_table = 'Parties'

class Candidates(models.Model):
    Candidate_ID = models.AutoField(primary_key=True)
    Candidate_Name = models.CharField(max_length=255)
    Party_ID = models.ForeignKey(Parties, on_delete=models.SET_NULL, null=True)
    Constituency_ID = models.ForeignKey(Constituencies, on_delete=models.CASCADE)
    Election_Year = models.IntegerField()
    Candidate_Description = models.TextField()

    class Meta:
        db_table = 'Candidates'

class Admins(models.Model):
    Admin_ID = models.AutoField(primary_key=True)
    Username = models.CharField(max_length=255)
    Password = models.CharField(max_length=255)
    First_Name = models.CharField(max_length=255)
    Last_Name = models.CharField(max_length=255)
    Email = models.EmailField(max_length=255)
    Role = models.CharField(max_length=20, choices=(('Superadmin', 'Superadmin'), ('Supervisor', 'Supervisor')))


    def authenticate_admin(username, password):
        try:
            admin = Admins.objects.get(Username=username)
            if admin.Password == password:
                return admin
        except Admins.DoesNotExist:
            return None
    class Meta:
        db_table = 'Admins'

class Logs(models.Model):
    Log_ID = models.AutoField(primary_key=True)
    Admin_ID = models.ForeignKey(Admins, on_delete=models.CASCADE)
    Action = models.CharField(max_length=255)
    Action_Date = models.DateTimeField()
    Action_Location = models.CharField(max_length=255)

    class Meta:
        db_table = 'Logs'

class Supervisor(models.Model):
    Supervisor_ID = models.AutoField(primary_key=True)
    Constituency_ID = models.ForeignKey(Constituencies, on_delete=models.CASCADE)
    Admin_ID = models.ForeignKey(Admins, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Supervisor'
class Voters(models.Model):
    Voter_ID = models.AutoField(primary_key=True)
    Username = models.CharField(max_length=255)
    Password = models.CharField(max_length=255)
    Email = models.EmailField(max_length=255)
    Registration_Date = models.DateTimeField()
    Last_Login = models.DateTimeField(null=True)
    Verified = models.CharField(max_length=3, choices=(('Yes', 'Yes'), ('No', 'No')), default='No')
    # Verified_By = models.ForeignKey(Supervisor, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'Voters'
    
    def authenticate_voter(username, password):
        try:
            voter = Voters.objects.get(Username=username)
            if voter.Password == password:
                return voter
        except Voters.DoesNotExist:
            return None

class Voter_Details(models.Model):
    Voter_Detail_ID = models.AutoField(primary_key=True)
    Voter_ID = models.ForeignKey(Voters, on_delete=models.CASCADE)
    First_Name = models.CharField(max_length=255)
    Last_Name = models.CharField(max_length=255)
    Date_of_Birth = models.DateField(null=True)
    Address = models.TextField()
    Contact_Number = models.CharField(max_length=15)
    Voter_Card_Number = models.CharField(max_length=20)
    Constituency_ID = models.ForeignKey(Constituencies,on_delete=models.CASCADE)

    class Meta:
        db_table = 'Voter_Details'

class Voted(models.Model):
    Voted_ID = models.AutoField(primary_key=True)
    Voter_ID = models.ForeignKey(Voters, on_delete=models.CASCADE)
    Candidate_ID = models.ForeignKey(Candidates, on_delete=models.CASCADE)
    Vote_Date = models.DateTimeField()

    class Meta:
        db_table = 'Voted'

class Election(models.Model):
    Election_ID = models.AutoField(primary_key=True)
    Election_Year = models.IntegerField()
    Constituency_ID = models.ForeignKey(Constituencies, on_delete=models.CASCADE)
    Election_Schedule = models.DateTimeField()
    Election_Status = models.CharField(max_length=20)

    class Meta:
        db_table = 'Election'


