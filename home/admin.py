from django.contrib import admin
from .models import Member, Experience, Lecturer, Review, Subject

admin.site.register(Member)
admin.site.register(Experience)
admin.site.register(Lecturer)
admin.site.register(Subject)
admin.site.register(Review)

