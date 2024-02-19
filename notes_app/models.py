from django.db import models
from django.contrib.auth.models import User

# Note model to create notes
class Note(models.Model):
    title = models.CharField(max_length=150, default=None)
    content = models.TextField(default=None)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')

    def __str__(self):
        return self.title
    

# Model to take note of to whom the note is shared    
class sharedNote(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='shared_note')
    shared_with = models.ManyToManyField(User, related_name='shared_note')
    shared_time = models.DateTimeField(auto_now_add=True)


# Model to save changes in Note
class noteHistory(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='notes_history')
    content = models.TextField()
    updated_time = models.DateTimeField(auto_now_add=True)