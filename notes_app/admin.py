from django.contrib import admin
from .models import Note, sharedNote, noteHistory

# Register your models here.
admin.site.register(Note)
admin.site.register(sharedNote)
admin.site.register(noteHistory)