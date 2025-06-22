from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from .models import Question, TriviaAttempt, Profile, QuestionChoice, QuestionAnswer
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import UserRegisterForm, ProfileForm, QuestionCreationForm, CategoryFilterForm, QuestionEditForm
from django.views import View
from django.utils import timezone
from django.views.generic.edit import FormView
from django.urls import reverse

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trivia_attempts'] = TriviaAttempt.objects.filter(user=self.object.user).order_by('-attempt_date')
        return context
    
# View that lets staff users create questions
class QuestionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Question
    form_class = QuestionCreationForm
    template_name = 'project/question_creation.html'

    
    def test_func(self):
        # Checks if logged in user is staff
        return self.request.user.is_staff

    def form_valid(self, form):
        question = form.save(commit=False) # Creates a question object from form data but doesn't save yet
        question.question_creator = self.request.user # Assigns logged in user as quesetion creator
        question.save() # Saves question to db with question creator added

        # Gets question choices from form and creates the 4 choices
        choices = [
            form.cleaned_data['choice1'],
            form.cleaned_data['choice2'],
            form.cleaned_data['choice3'],
            form.cleaned_data['choice4'],
        ]
        correct_ind = int(form.cleaned_data['correct_choice']) - 1 # correct choice index

        # Loop and save each question choice
        for i, c_text in enumerate(choices):
            QuestionChoice.objects.create(
                question=question,
                choice_text=c_text,
                correct_choice=(i == correct_ind)
            )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('question_detail', kwargs={'pk': self.object.pk}) # Redirects user to question detail page of the created question

# View that handles the displaying of trivia questions as well as processing submission
class TriviaAttemptView(LoginRequiredMixin, View):
    template_name = 'project/trivia_attempt.html'


    def get(self, request, category):
        # Get request to display trivia questions based on selected category
        questions = Question.objects.filter(category=category) # Gets all the questions in a category 
        return render(request, self.template_name, {
            'category': category,
            'questions': questions,
        }) # Passes category and questions to the template
    
    def post(self, request, category):
        # Post request for when the user submits their trivia attempt
        questions = Question.objects.filter(category=category)
        score = 0 # Initialized score

        trivia_attempt = TriviaAttempt.objects.create(
            user=request.user,
            category=category,
            score=0,
            attempt_date=timezone.now() 
        ) # Trivia attempt object with initial score value 0

        # Iteration through all of the questions to process the user's answers
        for question in questions:
            chosen_choice_id = request.POST.get(f'question_{question.id}') # Extracts user's chosen answer
            if chosen_choice_id: # if a choice was selected by the user
                chosen_choice = QuestionChoice.objects.get(id=chosen_choice_id) # Get the choice
                QuestionAnswer.objects.create(
                    trivia_attempt=trivia_attempt,
                    question=question,
                    user_choice=chosen_choice,
                    ) # Creates a QuestionAnswer object for user's answer
                if chosen_choice.correct_choice:
                    score += 5 # Add 5 points to score if user made the correct choice

        # After looping through questions, this saves the final score to the trivia attempt
        trivia_attempt.score = score
        trivia_attempt.save()

        return redirect('attempt_detail', pk=trivia_attempt.pk) # Redirect user to the attempt detail page showing their attempt

# View for displaying the leaderboards of best trivia scores
class TriviaLeaderboardView(FormView):
    template_name = 'project/trivia_leaderboard.html'
    form_class = CategoryFilterForm

    def form_valid(self, form):
        chosen_category = form.cleaned_data['category']

        if chosen_category == CategoryFilterForm.all_categories: # If user selects all categories, display leaderboard for all categories combined
            best_attempts = TriviaAttempt.objects.order_by('-score')[:10]

        else:
            best_attempts = TriviaAttempt.objects.filter(category=chosen_category).order_by('-score')[:10] # View leaderboards for specific categories

        context = self.get_context_data(
            form=form,
            chosen_category=chosen_category,
            best_attempts=best_attempts,
        )
        
        return render(self.request, self.template_name, context) # Render a template with updated context

# View for editing a question only accessible to staff users
class QuestionEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    form_class = QuestionEditForm
    template_name = 'project/edit_question.html'
    context_object_name = 'question'

    # Only accessible to staff users
    def test_func(self):
        return self.request.user.is_staff
    
    # Add choices to the context to be able to render and edit in template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['choices'] = self.object.choices.all()
        return context
    
    # When form is submitted and valid
    def form_valid(self, form):
        question = self.object # Question being edited
        choices = question.choices.all() # Choices being editted

        # Loops through choices to be able to update its text and if it's the correct choice
        for choice in choices:
            choice_text = self.request.POST.get(f'choice_{choice.id}')
            choice_is_correct = self.request.POST.get('correct_choice') == str(choice.id)
            if choice_text:
                choice.choice_text = choice_text
                choice.correct_choice = choice_is_correct
                choice.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('question_detail', kwargs={'pk': self.object.pk}) # Directs user to the question detail page upon a successful question update


    





