from django.db import models
from django.utils import timezone

# Create your models here.

# Creates a profile model that gives details of the user's profile information
class Profile(models.Model):
  first_name = models.CharField(blank=False)
  last_name = models.CharField(blank=False)
  city = models.CharField(blank=False)
  email= models.EmailField(blank=False)
  profile_image_url = models.URLField(blank=False)

  def get_status_messages(self):
    return self.statusmessage_set.all().order_by('-timestamp')


class StatusMessage(models.Model):
  timestamp = models.DateTimeField(default=timezone.now)
  message = models.TextField()
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.message} {self.timestamp.strftime('%B %d %Y, %I:%M %p')}."  





