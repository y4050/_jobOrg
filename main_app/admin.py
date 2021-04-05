from django.contrib import admin
from .models import Jobs, JobsCat, Saved, Note

# Register your models here.
admin.site.register(Jobs)
admin.site.register(JobsCat)
admin.site.register(Saved)
admin.site.register(Note)
