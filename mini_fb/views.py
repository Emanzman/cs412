from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from .forms import CreateProfileForm, CreateStatusMessageForm
from .models import Profile, StatusMessage
from django.urls import reverse


# Create your views here.

class ShowAllProfilesView(ListView):
# View to display a list of all the user profiles

  model = Profile
  template_name = 'mini_fb/show_all_profiles.html'
  context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
# View to display a single user profile
  model = Profile
  template_name = 'mini_fb/show_profile.html'
  context_object_name = 'profile'


class CreateProfileView(CreateView):
# View to create a new profile with a form 
  model = Profile
  template_name="mini_fb/create_profile_form.html"
  form_class = CreateProfileForm

class CreateStatusMessageView(CreateView):
  # View to create a new status message with a form that is linked to a specifc profile.
  model = StatusMessage
  template_name="mini_fb/create_status_form.html"
  form_class = CreateStatusMessageForm


  def get_context_data(self):
    # Adds the profile object to the context dictionary and returns context for use in the template
    context = super().get_context_data() # Calls superclass method and gets context dicitonary.
    pk = self.kwargs['pk'] # Gets primary key from the url
    profile = Profile.objects.get(pk=pk) # Gets profile object using the primary key.
    context['profile'] = profile # Adds a profile to context dictionary
    return context
  
  def form_valid(self, form):
      # Associates the status message to the specific user profile
      pk = self.kwargs['pk'] # Gets primary key from the url
      profile = Profile.objects.get(pk=pk) # Gets profile object using the primary key.
      form.instance.profile = profile # Associates the profile to the status message.
      return super().form_valid(form) # Calls superclass method and submits the form if valid.
  
  def get_success_url(self):
      # Returns a url that page gets redirected to after creating a new status
      pk = self.kwargs['pk']
      return reverse('show_profile', kwargs={'pk':pk})







