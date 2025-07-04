from django.urls import path
from .views import QuestionListView, QuestionDetailView, TriviaAttemptListView, TriviaAttemptDetailView, CategorySelectionView, QuestionCategoryListView, ShowProfilePageView, CreateProfileView, RedirectToProfileView, QuestionCreateView, TriviaAttemptView, TriviaLeaderboardView, QuestionEditView, TriviaScoreGraphView, QuestionDeleteView, HomePageView
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

# Emmanuel Eyob emanzman@bu.edu

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('categories/', CategorySelectionView.as_view(), name='category_selection'),
    path('questions/', QuestionListView.as_view(), name='question_list'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    path('attempts/', TriviaAttemptListView.as_view(), name='attempt_list'),
    path('attempts/<int:pk>/', TriviaAttemptDetailView.as_view(), name='attempt_detail'),
    path('category/<str:category>/', QuestionCategoryListView.as_view(), name='category_questions'),
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('redirect/', RedirectToProfileView.as_view(), name='redirect_to_profile'),
    path('questions/create/', QuestionCreateView.as_view(), name='create_question'),
    path('trivia_attempt/<str:category>/', TriviaAttemptView.as_view(), name='trivia_attempt'),
    path('trivia_leaderboard/', TriviaLeaderboardView.as_view(), name='trivia_leaderboard'),
    path('questions/<int:pk>/edit/', QuestionEditView.as_view(), name='edit_question'),
    path('profile/<int:profile_pk>/triviascore-graph/<str:category>/', TriviaScoreGraphView.as_view(), name='triviascore_graph'),
    path('questions/<int:pk>/delete/', QuestionDeleteView.as_view(), name='delete_question'),



]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)