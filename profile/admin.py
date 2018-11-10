from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Qualifications)
admin.site.register(Preferences)
admin.site.register(Class)
admin.site.register(Instrument)


