from django.db import models
from apps.base.models import BaseModel
from apps.accounts.models import CustomUser

# Create your models here.

class Event(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=255)
    participants = models.ManyToManyField(CustomUser, related_name='events') 
    max_participants = models.PositiveIntegerField()
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    
    @property
    def status(self):
        if self.participants.count() >= self.max_participants:
            return 'Full'
        else:
            return 'Open'
    
    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        
    def __str__(self):
        return self.title   
    

