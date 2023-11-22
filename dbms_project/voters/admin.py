from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Voters)
admin.site.register(Voter_Details)
admin.site.register(Voted)
admin.site.register(Candidates)
admin.site.register(Supervisor)
admin.site.register(Logs)
admin.site.register(Parties)
admin.site.register(Constituencies)
admin.site.register(Admins)

