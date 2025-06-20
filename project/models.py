from django.db import models
from django.contrib.auth.models import User

# Models for Ethiopian Trivia App
# Create your models here.

# Adds additional fields to built-in Django User model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='project_profile') # One user can only have one profile
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Stores trivia questions, their category, creator info, and an optional image
class Question(models.Model):
  category_choices = [
        ('music', 'Music'),
        ('history', 'History'),
        ('geography', 'Geography'),
  ] # First value in tuple is the value stored in the database and the second value is the label shown thorughout the app and in the drop down menus
  
  question_text = models.TextField() 
  category = models.CharField(choices=category_choices)
  question_creator = models.ForeignKey(User, on_delete=models.CASCADE)
  image = models.ImageField(blank=True, null=True)

  def __str__(self):
    return self.question_text
  
# Stores and represent the multiple choices from each question 
class QuestionChoice(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
  choice_text = models.CharField()
  correct_choice = models.BooleanField(default=False)  

  def __str__(self):
    correct_checker = "Correct" if self.correct_choice else "Incorrect"
    return f"{self.choice_text} ({correct_checker})"

# Stores values related to a user's trivia attempt such as the user, category, trivia score, and the attempt date
class TriviaAttempt(models.Model):
  category__dropdown = Question.category_choices

  user = models.ForeignKey(User, on_delete=models.CASCADE)
  category = models.CharField(choices=category__dropdown)
  score = models.IntegerField()
  attempt_date = models.DateTimeField()

  def __str__(self):
    return f"{self.user.username} | Category: {self.category} | Score: {self.score}"

# Stores the answer the user chose from each multiple choice question attempt
class QuestionAnswer(models.Model):
  trivia_attempt = models.ForeignKey(TriviaAttempt, on_delete=models.CASCADE)
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  user_choice = models.ForeignKey(QuestionChoice, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.user_choice} | Question: {self.question} | User: {self.trivia_attempt}"
  




