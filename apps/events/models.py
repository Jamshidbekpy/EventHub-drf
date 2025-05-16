from apps.accounts.models import CustomUser
from apps.base.models import BaseModel
from django.utils.text import slugify
from django.db import models

# Create your models here.


class Event(BaseModel):
    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="owner_events"
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=255)
    participants = models.ManyToManyField(
        CustomUser, related_name="participated_events", through="EventParticipant"
    )
    max_participants = models.PositiveIntegerField()
    image = models.ImageField(upload_to="event_images/", null=True, blank=True)

    @property
    def status(self):
        if self.participants.count() >= self.max_participants:
            return "Full"
        else:
            return "Open"

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class EventParticipant(models.Model):
    """
    Event registration model
    """

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="event_registrations"
    )
    event = models.ForeignKey(
        Event, related_name="registrations", on_delete=models.CASCADE
    )
    registered_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "event")
        verbose_name = "Event Registration"
        verbose_name_plural = "Event Registrations"

    def str(self):
        return f"{self.user.username} - {self.event.title}"
