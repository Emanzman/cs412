from django.db import models
from datetime import datetime



# Create your models here.

class Voter(models.Model):
  last_name = models.CharField()
  first_name = models.CharField()
  street_number = models.CharField()
  street_name = models.CharField()
  apartment_number = models.CharField(blank=True, null=True)
  zip_code = models.CharField()
  date_of_birth = models.DateField()
  date_of_registration = models.DateField()
  party_affiliation = models.CharField(max_length=2)
  precinct_number = models.CharField()

  v20state = models.BooleanField()
  v21town = models.BooleanField()
  v21primary = models.BooleanField()
  v22general = models.BooleanField()
  v23town = models.BooleanField()
  voter_score = models.IntegerField()

  def __str__(self):
    return f'{self.first_name} {self.last_name} {self.street_number} {self.street_name} {self.apartment_number} {self.zip_code} {self.date_of_birth} {self.party_affiliation}'
  

def load_data():
  filename = '/Users/emmanueleyob/Desktop/django/newton_voters.csv'
  f = open(filename)
  f.readline()

  for line in f:
    fields = line.strip().split(',')
    try:
      voter = Voter(
        last_name = fields[1],
        first_name = fields[2],
        street_number = fields[3],
        street_name = fields[4],
        apartment_number = fields[5] if fields[5] else None,
        zip_code = fields[6],
        date_of_birth = datetime.strptime(fields[7], '%Y-%m-%d').date(),
        date_of_registration = datetime.strptime(fields[8], '%Y-%m-%d').date(),
        party_affiliation = fields[9],
        precinct_number = fields[10],

        v20state = (fields[11].strip() == 'TRUE'),
        v21town = (fields[12].strip() == 'TRUE'),
        v21primary = (fields[13].strip() == 'TRUE'),
        v22general = (fields[14].strip() == 'TRUE'),
        v23town = (fields[15].strip() == 'TRUE'),
        voter_score = fields[16],

      )
      voter.save()

    except Exception as exception:
      print(f'Skipped:{fields} because: {exception}')

  print(f'Done. Created {len(Voter.objects.all())} Results.')

  