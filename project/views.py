from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from .models import Question, TriviaAttempt, Profile, QuestionChoice
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import UserRegisterForm, ProfileForm, QuestionCreationForm
from django.views import View

# Views page for Ethiopian Trivia App.
# Create your views here.

# View that displays list of questions for users with staff privelleges
class QuestionListView(UserPassesTestMixin,ListView):
    model = Question
    template_name = 'project/question_list.html'
    context_object_name = 'questions'

    def test_func(self):
      # This checks if the authenticated user has staff privelleges
      return self.request.user.is_authenticated and self.request.user.is_staff
    
    def handle_no_permission(self):
        # Redirects users to homepage if they don't have staff privelleges
        return redirect('category_selection')

# View that displays a list of questions in a category 
class QuestionCategoryListView(ListView):
    model = Question
    template_name = 'project/question_list.html'
    context_object_name = 'questions'

    def get_queryset(self):
      category = self.kwargs['category']
      return Question.objects.filter(category=category)

# View displaying a list of categories to choose from
class CategorySelectionView(TemplateView):
    template_name = 'project/category_selection.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Question.category_choices
        return context

# View that displayes the details of a question and its choices
class QuestionDetailView(DetailView):
    model = Question
    template_name = 'project/question_detail.html'
    context_object_name = 'question'

# View that lists all trivia attempts from a user
class TriviaAttemptListView(ListView):
    model = TriviaAttempt
    template_name = 'project/triviaattempt_list.html'
    context_object_name = 'attempts'

# View that displays detailed information about a specific trivia attempt
class TriviaAttemptDetailView(DetailView):
    model = TriviaAttempt
    template_name = 'project/triviaattempt_detail.html'
    context_object_name = 'attempt'

# View that handles user registration and profile creation together
class CreateProfileView(CreateView):   
    template_name = 'project/create_profile_form.html'

    def get(self, request, *args, **kwargs):
        # Redirects user to their profile page if they are logged in and have a proifle
        if request.user.is_authenticated and Profile.objects.filter(user=request.user).exists():
            profile = Profile.objects.get(user=request.user)
            return redirect('show_profile', pk=profile.pk)
        
        # Renders registration and profile forms that are blank
        user_form = UserRegisterForm()
        profile_form = ProfileForm()
        return render(request, self.template_name, {
            'form': user_form,
            'profile_form': profile_form
        })

    def post(self, request, *args, **kwargs):
        # Handles new user and profile registration forms
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save() # Saves form
            login(request, user) # Logs user in
            profile = profile_form.save(commit=False) # Creates profile instance but doesn't save to database yet
            profile.user = user # Links profile to user
            profile.save() # Saves profile
            return redirect('show_profile', pk=profile.pk) # Redirects to user's profile page
        
        # Renders form again if the form is invalid
        return render(request, self.template_name, {
            'form': user_form,
            'profile_form': profile_form
        })
    
# View that redirects logged in users to their profile page if it exists and if it doesn't exist, it redirects them to the profile creation page
class RedirectToProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
            return redirect('show_profile', pk=profile.pk)
        except Profile.DoesNotExist:
            return redirect('create_profile')

# View that shows a user's profile with the profile model
class ShowProfilePageView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'project/profile.html'
    context_object_name = 'profile'

# View that lets staff users create trivia questions with choices and other question information
class QuestionCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'project/question_creation.html'

    def test_func(self):
        # Restricts access to page to staff users only
        return self.request.user.is_staff


    def get(self, request):
        # Renders question creation form that is empty
        form = QuestionCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # Proceses question creation form
        form = QuestionCreationForm(request.POST, request.FILES)

        if form.is_valid():
            # Creates question object
            question = Question.objects.create(
                question_text=form.cleaned_data['question_text'],
                category=form.cleaned_data['category'],
                image=form.cleaned_data.get('image'),
                question_creator=request.user
            )
            # Gets question choices from form and creates the 4 choices
            choices = [
                form.cleaned_data['choice1'],
                form.cleaned_data['choice2'],
                form.cleaned_data['choice3'],
                form.cleaned_data['choice4'],
            ]
            correct_ind = int(form.cleaned_data['correct_choice']) - 1 # Index of correct choice

            # Loop and save each question choice
            for i, c_text in enumerate(choices):
                QuestionChoice.objects.create(
                    question=question,
                    choice_text=c_text,
                    correct_choice=(i == correct_ind)
                )

            return redirect('question_detail', pk=question.pk) # Redirects user to question detail page of the created question

        return render(request, self.template_name, {'form': form}) # If form is invalid, re-render the form