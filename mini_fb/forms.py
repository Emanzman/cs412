from django import forms
from .models import Profile, StatusMessage


class CreateProfileForm(forms.ModelForm):
# Form leting users create a profile and fields of form are specifiied.

  first_name = forms.CharField(label="First Name", required=True)
  last_name = forms.CharField(label="Last Name", required=True)
  city = forms.CharField(label="City", required=True)
  email= forms.EmailField(label="Email", required=True)
  profile_image_url = forms.URLField(label="Profile Image URL", required=True)


  class Meta:
    # States which model this form is connected to and includes relevant fields.
    model = Profile
    fields = ['first_name', 'last_name', 'city', 'email', 'profile_image_url']

class CreateStatusMessageForm(forms.ModelForm):
# Form that lets userse create a status message and message form field is specified.
  message = forms.CharField(label= "Message", required=True)

  class Meta:
  # States which model this form is connected to and includes relevant fields.
    model = StatusMessage
    fields = ['message']

  
class UpdateProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['city', 'email', 'profile_image_url']

  