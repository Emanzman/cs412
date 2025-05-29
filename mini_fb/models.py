from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.

# Creates a profile model that gives details of the user's profile information
class Profile(models.Model):
  first_name = models.CharField(blank=False)
  last_name = models.CharField(blank=False)
  city = models.CharField(blank=False)
  email= models.EmailField(blank=False)
  profile_image_url = models.URLField(blank=False)

  def get_status_messages(self):
    return StatusMessage.objects.filter(profile=self).order_by('-timestamp')
  
  def get_absolute_url(self):
    return reverse("show_profile", kwargs={"pk": self.pk})


class StatusMessage(models.Model):
  timestamp = models.DateTimeField(default=timezone.now)
  message = models.TextField()
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.message} {self.timestamp.strftime('%B %d %Y, %I:%M %p')}."  





