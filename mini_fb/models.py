from django.db import models

# Create your models here.

# Creates a profile model that gives details of the user's profile information
class Profile(models.Model):
  first_name = models.CharField(blank=False)
  last_name = models.CharField(blank=False)
  city = models.CharField(blank=False)
  email= models.EmailField(blank=False)
  profile_image_url = models.URLField(blank=False)




