from django.shortcuts import render, redirect
from django.views.generic import ListView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm
from .models import Profile, StatusMessage, Image, StatusImage
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

# Views page that offers the ability to modify profiles, modift status messages, and more
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

class CreateStatusMessageView(LoginRequiredMixin, CreateView):
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
      
      sm = form.save() # Saves form and stores in a db
      files = self.request.FILES.getlist('files') # Reads file from form

      for file in files:
         image = Image(profile=sm.profile, image_file=file) # Creation of an image object
         image.save()

         status_image = StatusImage(image=image, status_message=sm) # Creation of a StatusImage object
         status_image.save()
         
      return super().form_valid(form) # Calls superclass method and submits the form if valid.
  
  def get_success_url(self):
      # Returns a url that page gets redirected to after creating a new status
      pk = self.kwargs['pk']
      return reverse('show_profile', kwargs={'pk':pk})


class UpdateProfileView(LoginRequiredMixin, UpdateView):
   # A view to update a user profile through a form
   model = Profile
   template_name = 'mini_fb/update_profile_form.html'
   form_class = UpdateProfileForm

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
   # A view to delete a status message
   model = StatusMessage
   template_name = 'mini_fb/delete_status_form.html'
   context_object_name = 'status'

   def get_success_url(self):
      # URL redirection after a deleted status message
      pk = self.object.profile.pk
      return reverse('show_profile', kwargs={'pk':pk})
   
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
   # A view to update a status message through a form
   model = StatusMessage
   template_name = 'mini_fb/update_status_form.html'
   form_class = CreateStatusMessageForm
   context_object_name = 'status'

   def get_success_url(self):
      # URL redirection after an updated status message
      pk = self.object.profile.pk
      return reverse('show_profile', kwargs={'pk':pk})
      
class AddFriendView(LoginRequiredMixin, View):
   def dispatch(self, request, *args, **kwargs):
      # Creates a friendship relationship and redirects user to the profile page of the profile that added the friend.
      p1_pk = self.kwargs['pk']
      p2_pk = self.kwargs['other_pk']
      
      profile1 = Profile.objects.get(pk=p1_pk)
      profile2 = Profile.objects.get(pk=p2_pk)

      profile1.add_friend(profile2)

      return redirect('show_profile', pk= p1_pk)
      

class ShowFriendSuggestionView(LoginRequiredMixin, DetailView):
   # A view for showing the friend suggestions
   model = Profile
   template_name='mini_fb/friend_suggestions.html'
   context_object_name= 'profile'


class ShowNewsFeedView(LoginRequiredMixin, DetailView):
   # A view for showing a profiles news feed
   model = Profile
   template_name= 'mini_fb/news_feed.html'
   context_object_name= 'profile'