from django.contrib import admin

from .models import Profile, Question, QuestionChoice, TriviaAttempt, QuestionAnswer

# Register your models here.

class QuestionChoiceInline(admin.TabularInline):
  model = QuestionChoice
  extra = 4

class QuestionAdmin(admin.ModelAdmin):
  inlines = [QuestionChoiceInline]

admin.site.register(Profile)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionChoice)
admin.site.register(TriviaAttempt)
admin.site.register(QuestionAnswer)
