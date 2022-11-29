from django.contrib import admin

# Register your models here.
from .models import Poll, Candidate, Criteria, Score

admin.site.register(Poll)
admin.site.register(Candidate)
admin.site.register(Criteria)
admin.site.register(Score)
