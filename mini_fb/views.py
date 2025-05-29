from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from .forms import CreateProfileForm
from .models import Profile

# Create your views here.

# View to display a list of all the user profiles
class ShowAllProfilesView(ListView):
  model = Profile
  template_name = 'mini_fb/show_all_profiles.html'
  context_object_name = 'profiles'

# View to display a single user profile
class ShowProfilePageView(DetailView):
  model = Profile
  template_name = 'mini_fb/show_profile.html'
  context_object_name = 'profile'

class CreateProfileView(CreateView):
  model = Profile
  template_name="mini_fb/create_profile_form.html"
  form_class = CreateProfileForm




