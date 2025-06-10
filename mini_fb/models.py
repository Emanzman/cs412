from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User


# Defines the data models being used in the Mini Facebook web app
# Create your models here.

class Profile(models.Model):
  # Creates a profile model that gives details of the user's profile information.
 
  first_name = models.CharField(blank=False)
  last_name = models.CharField(blank=False)
  city = models.CharField(blank=False)
  email= models.EmailField(blank=False)
  profile_image_url = models.URLField(blank=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)



  def get_status_messages(self):
    # Returns all the status messages from the specific profile in order from newest to oldest.
    return StatusMessage.objects.filter(profile=self).order_by('-timestamp')
  
  def get_absolute_url(self):
    # Calls reverse and returns a URL for the specific profile.
    return reverse("show_profile", kwargs={"pk": self.pk})
  
  def get_friends(self):
    # Returns a list of all friends profiles
    friends_profile1 = Friend.objects.filter(profile1=self)
    friends_profile2 = Friend.objects.filter(profile2=self)

    friends_list = []

    for friend in friends_profile1:
      friends_list.append(friend.profile2)

    for friend in friends_profile2:
      friends_list.append(friend.profile1)

    return friends_list
  
  def add_friend(self, other):
    # Builds a friend relationship between two profiles if friendship doesn't already exist
    if self == other:
      return
    
    friendship = Friend.objects.filter(Q(profile1=self, profile2=other) | Q(profile2=self, profile1=other)).exists() #  Checks if there is a friendship from both sides of the profiles

    if not friendship:
      Friend.objects.create(profile1=self, profile2=other) # Creates a friendship if it doesn't already exist

  def get_friend_suggestions(self):
      friend_suggestions = Profile.objects.exclude(pk=self.pk).exclude(pk__in=[friend.pk for friend in self.get_friends()]) # Friend suggestions that excludes the profile itself and current friends of the profile
      return friend_suggestions

  def get_news_feed(self):
    # Returns a list of status messages of the profile and their friends
    feed_profiles = [self] + self.get_friends() # list addition
    return StatusMessage.objects.filter(profile__in=feed_profiles).order_by('-timestamp')


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

class Friend(models.Model):
  # Model that defines a friendship between two profiles
  profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile1')
  profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile2')
  timestamp = models.DateTimeField(default=timezone.now)
  
  def __str__(self):
    return f"{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}" # String representation of friend relationship



