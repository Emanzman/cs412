from . import views
from django.urls import path


urlpatterns = [
  path(r'', views.quote, name="quote"),
  path(r'quote/', views.quote, name="quote"),
  path(r'show_all/', views.show_all, name="show_all"),
  path(r'about/', views.about, name="about"),
]
