from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TripDb(models.Model):
    title = models.CharField(max_length=150)
    start_date = models.DateField()
    destination = models.CharField(max_length=150)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE , related_name='created_trips')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title