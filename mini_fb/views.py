from django.shortcuts import render, redirect
from django.views.generic import ListView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm
from .models import Profile, StatusMessage, Image, StatusImage
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

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

  def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs) # Calls super() method and gets context dictionary
     context['user_creation_form'] = kwargs.get('user_creation_form', UserCreationForm()) #Adds user_creation_form to a context dictionary
     return context

  def form_valid(self, form):
     user_creation_form = UserCreationForm(self.request.POST) # Reconstructs user creation form with self.request.POST data

     if user_creation_form.is_valid(): # Checks if the user creation form is valid
        user = user_creation_form.save() # saves user creation form
        login(self.request, user) # Logs the user in
        form.instance.user = user # attaches Django user to Profile instance object
        return super().form_valid(form) # delegates rest of the work to superclass
     
  def get_success_url(self):
     profile = Profile.objects.get(user=self.request.user)
     return reverse('show_profile', kwargs={'pk': profile.pk}) # Redirects to the new user's profile page


class CreateStatusMessageView(LoginRequiredMixin, CreateView):
  # View to create a new status message with a form that is linked to a specifc profile.
  model = StatusMessage
  template_name="mini_fb/create_status_form.html"
  form_class = CreateStatusMessageForm


  def get_context_data(self):
    # Adds the profile object to the context dictionary and returns context for use in the template
    context = super().get_context_data() # Calls superclass method and gets context dicitonary.
    context['profile'] = self.get_object() # Adds a profile to context dictionary
    return context
  
  def form_valid(self, form):
      
      # Associates the status message to the specific user profile
      profile = self.get_object() # Gets profile object using the primary key.
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
      profile = self.get_object()
      return reverse('show_profile', kwargs={'pk': profile.pk})
  
  def get_login_url(self):
      return reverse('login') # Redirects to login page

  def get_object(self):
     return Profile.objects.get(user=self.request.user) # Replaces pk usage to get an object
  


class UpdateProfileView(LoginRequiredMixin, UpdateView):
   # A view to update a user profile through a form
   model = Profile
   template_name = 'mini_fb/update_profile_form.html'
   form_class = UpdateProfileForm

   def get_object(self):
      return Profile.objects.get(user=self.request.user) # Replaces pk usage to get an object
   
   def get_login_url(self):
      return reverse('login') # Redirects to login page

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
   # A view to delete a status message
   model = StatusMessage
   template_name = 'mini_fb/delete_status_form.html'
   context_object_name = 'status'

   def get_success_url(self):
      # URL redirection after a deleted status message
      pk = self.object.profile.pk
      return reverse('show_profile', kwargs={'pk': pk})
   
   def get_login_url(self):
      return reverse('login') # Redirects to login page
   
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
   # A view to update a status message through a form
   model = StatusMessage
   template_name = 'mini_fb/update_status_form.html'
   form_class = CreateStatusMessageForm
   context_object_name = 'status'

   def get_success_url(self):
      # URL redirection after an updated status message
      pk = self.object.profile.pk
      return reverse('show_profile', kwargs={'pk': pk})
   
   def get_login_url(self):
      return reverse('login') # Redirects to login page
      
class AddFriendView(LoginRequiredMixin, View):
   def dispatch(self, request, *args, **kwargs):
      # Creates a friendship relationship and redirects user to the profile page of the profile that added the friend.
      p2_pk = self.kwargs['other_pk']
      
      profile1 = Profile.objects.get(user=request.user)
      profile2 = Profile.objects.get(pk=p2_pk)

      profile1.add_friend(profile2)

      return redirect('show_profile',pk=profile1.pk)
   
   def get_object(self):
      return Profile.objects.get(user=self.request.user) # Replaces pk usage to get an object

   def get_login_url(self):
      return reverse('login') # Redirects to login page  

class ShowFriendSuggestionView(LoginRequiredMixin, DetailView):
   # A view for showing the friend suggestions
   model = Profile
   template_name='mini_fb/friend_suggestions.html'
   context_object_name= 'profile'

   def get_object(self):
     return Profile.objects.get(user=self.request.user) # Replaces pk usage to get an object

   def get_login_url(self):
      return reverse('login') # Redirects to login page


class ShowNewsFeedView(LoginRequiredMixin, DetailView):
   # A view for showing a profiles news feed
   model = Profile
   template_name= 'mini_fb/news_feed.html'
   context_object_name= 'profile'

   def get_object(self):
     return Profile.objects.get(user=self.request.user) # Replaces pk usage to get an object

   def get_login_url(self):
      return reverse('login') # Redirects to login page