from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import TriviaAttempt, Profile, Question, QuestionChoice

# Form page for Ethiopian Trivia App

# Form that handles user registration
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        # Values displayed in the registration form
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

# Adding a profile image upload form to be combined with the user creation form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

# Form to create and modify a trivia attempt
class TriviaAttemptForm(forms.ModelForm):
    class Meta:
        model = TriviaAttempt
        fields = ['category', 'score']

# Form to create a trivia question with question text, category, choices, and an optional image
class QuestionCreationForm(forms.ModelForm):

    # Fields to enter 4 choices for the question
    choice1 = forms.CharField(label='Choice 1')
    choice2 = forms.CharField(label='Choice 2')
    choice3 = forms.CharField(label='Choice 3')
    choice4 = forms.CharField(label='Choice 4')

    # Radio button selection of the correct choice
    correct_choice = forms.ChoiceField(
        label='Correct Choice',
        choices=[('1', 'Choice 1'), ('2', 'Choice 2'), ('3', 'Choice 3'), ('4', 'Choice 4')],
        widget=forms.RadioSelect
    )
    class Meta:
        model = Question
        fields = ['question_text', 'category', 'image']

# From used for category dropdown on leaderboard page
class CategoryFilterForm(forms.Form):
    all_categories = 'all'
    category = forms.ChoiceField(choices=[('', 'Choose a category'), (all_categories, 'All Categories'),] + list(Question.category_choices), required=True)

# From uses for editting a question
class QuestionEditForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'category', 'image']