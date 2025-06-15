from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
from datetime import datetime
import plotly.graph_objs as go
from plotly.offline import plot
from collections import Counter

# Create your views here.
# Views for viewing voter lists, each voter's detail, and graph representations of data

class VoterListView(ListView):
  # Displayes list of voters that can be filtered
  template_name = 'voter_analytics/voter_filter.html'
  model = Voter
  context_object_name= 'voters'
  paginate_by = 100

  def get_queryset(self):
    voters = super().get_queryset()
    # Party Affiliation Filter
    if 'party' in self.request.GET:
      party = self.request.GET.get('party')
      if party:
        voters = voters.filter(party_affiliation=party)
    
    # Minimum Year of Birth Filter
    if 'min_dob' in self.request.GET:
      min_dob = self.request.GET.get('min_dob')
      if min_dob:
        voters = voters.filter(date_of_birth__gt=datetime(int(min_dob), 1, 1))

    # Maximum Year of Birth Filter
    if 'max_dob' in self.request.GET:
      max_dob = self.request.GET.get('max_dob')
      if max_dob:
        voters = voters.filter(date_of_birth__lt=datetime(int(max_dob), 12, 31))

    # Voter Score Filter
    if 'voter_score' in self.request.GET:
      voter_score = self.request.GET.get('voter_score')
      if voter_score:
        voters = voters.filter(voter_score=voter_score)

    # Election Participation Filter
    elections = {
            'v20state': self.request.GET.get('v20state'),
            'v21town': self.request.GET.get('v21town'),
            'v21primary': self.request.GET.get('v21primary'),
            'v22general': self.request.GET.get('v22general'),
            'v23town': self.request.GET.get('v23town'),
        }

    for election, val in elections.items():
      if val == 'on': # If the checkbox is cheked
        voters = voters.filter(**{election: True}) # Includes election in filter

    return voters

  def get_context_data(self, **kwargs):
    # Adds list of unique values to filter with through a dropdown option per category
    context = super().get_context_data(**kwargs)
    context['party_options'] = sorted(set(v.party_affiliation for v in Voter.objects.all()))
    context['dob_years'] = sorted(set(v.date_of_birth.year for v in Voter.objects.all()))
    context['score_options'] = sorted(set(v.voter_score for v in Voter.objects.all()))

    return context


class VoterDetailView(DetailView):
  # View for single voter information
  template_name='voter_analytics/voter_details.html'
  model = Voter
  context_object_name= 'voter'


class GraphView(ListView):
  # Graph display for voter information
  template_name = 'voter_analytics/graphs.html'
  model = Voter
  context_object_name = 'voters'

  def get_queryset(self):
    # Repeat of earlier get_queryset implementation for usage in GraphView
    voters = super().get_queryset()

    # Party Affiliation Filter    
    if 'party' in self.request.GET:
      party = self.request.GET.get('party')
      if party:
        voters = voters.filter(party_affiliation=party)
    # Minimum Year of Birth Filter
    if 'min_dob' in self.request.GET:
      min_dob = self.request.GET.get('min_dob')
      if min_dob:
        voters = voters.filter(date_of_birth__gt=datetime(int(min_dob), 1, 1))

    # Maximum Year of Birth Filter
    if 'max_dob' in self.request.GET:
      max_dob = self.request.GET.get('max_dob')
      if max_dob:
        voters = voters.filter(date_of_birth__lt=datetime(int(max_dob), 12, 31))
    
    # Voter Score Filter
    if 'voter_score' in self.request.GET:
      voter_score = self.request.GET.get('voter_score')
      if voter_score:
        voters = voters.filter(voter_score=voter_score)

    # Election Participation Filter
    elections = {
            'v20state': self.request.GET.get('v20state'),
            'v21town': self.request.GET.get('v21town'),
            'v21primary': self.request.GET.get('v21primary'),
            'v22general': self.request.GET.get('v22general'),
            'v23town': self.request.GET.get('v23town'),
        }

    for election, val in elections.items():
      if val == 'on': # If the checkbox is cheked
        voters = voters.filter(**{election: True}) # Includes election in filter

    return voters

  def get_context_data(self, **kwargs):
    # Adds list of unique values to filter with through a dropdown option per category
    context = super().get_context_data(**kwargs)
    voters = context['voters']
    context['party_options'] = sorted(set(v.party_affiliation for v in Voter.objects.all()))
    context['dob_years'] = sorted(set(v.date_of_birth.year for v in Voter.objects.all()))
    context['score_options'] = sorted(set(v.voter_score for v in Voter.objects.all()))

    # Year of Birth Histogram
    birth_year_data = [v.date_of_birth.year for v in voters] # Made a list of birth date year for each voter
    year_counts = Counter(birth_year_data) # Counts the  amount of voters born in each year
    birth_histogram = go.Bar(x=list(year_counts.keys()), y=list(year_counts.values())) # Creates a histogram with birth year on the x-axis and count of them on the y-axis
    birth_year_layout = go.Layout(title='Voters by their Year of Birth', xaxis=dict(title='Year'), yaxis=dict(title='Voter Count')) # Labels and title for histogram
    birth_year_figure = go.Figure(data=[birth_histogram], layout=birth_year_layout) # Use the data and layout to use as a Plotly figure
    context['birth_year_histogram'] = plot(birth_year_figure, output_type='div') # Context to use in template

    # Party Affiliation Pie Chart 
    party_aff_counts = Counter(v.party_affiliation for v in voters) # Counts number of voters per party affiliation
    party_pie_chart = go.Pie(labels=list(party_aff_counts.keys()), values=list(party_aff_counts.values())) # Creates a pie chart with party as the label and counts as the values
    party_figure = go.Figure(data=[party_pie_chart]) # Use pie chart as a Plotly figure
    party_figure.update_layout(title='Voters by their Party Affiliation') # Pie chart title
    context['party_affiliation_pie_chart'] = plot(party_figure, output_type='div') # Context to use in template

    # Election Participation Histogram 
    elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town'] # Election fields
    participation_counts = {election: voters.filter(**{election: True}).count() for election in elections} # Dictionary counting how many voters participated in each election
    election_histogram = go.Bar(x=list(participation_counts.keys()), y=list(participation_counts.values())) # Creates histogram with election name and their counts
    election_figure = go.Figure(data=[election_histogram]) # Used histogram as a Plotly figure
    election_figure.update_layout(title='Voters by their Participation in Elections', xaxis=dict(title='Election'), yaxis=dict(title='Number of Voters')) # Lables and title for histogram
    context['election_participation_histogram'] = plot(election_figure, output_type='div') # Context to use in template
  
    return context




  