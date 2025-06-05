from django.db import models
from django.utils import timezone
from django.urls import reverse

# Defines the data models being used in the Mini Facebook web app
# Create your models here.

class Profile(models.Model):
  # Creates a profile model that gives details of the user's profile information.
 
  first_name = models.CharField(blank=False)
  last_name = models.CharField(blank=False)
  city = models.CharField(blank=False)
  email= models.EmailField(blank=False)
  profile_image_url = models.URLField(blank=False)


  def get_status_messages(self):
    # Returns all the status messages from the specific profile in order from newest to oldest.
    return StatusMessage.objects.filter(profile=self).order_by('-timestamp')
  
  def get_absolute_url(self):
    # Calls reverse and returns a URL for the specific profile.
    return reverse("show_profile", kwargs={"pk": self.pk})


class StatusMessage(models.Model):
  # Creates a status model that represents a status that is from a specifc user profile.
  timestamp = models.DateTimeField(default=timezone.now)
  message = models.TextField()
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE) # Deletes if profile deleted.

  def __str__(self):
    # Returns a string that displays the status message along with the datae and time.
    return f"{self.message} {self.timestamp.strftime('%B %d %Y, %I:%M %p')}."

  def get_images(self):
    # Returns images from this status message
    return Image.objects.filter(statusimage__status_message=self)  

class Image(models.Model):
  # Model that represents and image uploaded from a profile
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
  image_file = models.ImageField()
  timestamp = models.DateTimeField(default=timezone.now)
  caption = models.CharField(blank=True)

class StatusImage(models.Model):
  # Model that finds which status image is related to which image
  image = models.ForeignKey(Image, on_delete=models.CASCADE)
  status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)



