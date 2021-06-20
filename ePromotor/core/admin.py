from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, DeanWorker, Promoter, Student, File, Record


# Models registered to admin panel
admin.site.register(User)
admin.site.register(DeanWorker)
admin.site.register(Promoter)
admin.site.register(Student)
admin.site.register(File)
admin.site.register(Record)

# Models not registered to admin panel
admin.site.unregister(Group)
