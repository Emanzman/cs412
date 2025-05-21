from django.shortcuts import render
import random

# Create your views here.

quotes_list = ["Darkness cannot drive out darkness, only light can do that. Hate cannot drive out hate, only love can do that.",
               "The ultimate measure of a man is not where he stands in moments of comfort and convenience, but where he stands at times of challenge and controversy.",
               "True peace is not merely the absence of tension; it is the presence of justice.",
               "In the end, we will remember not the words of our enemies, but the silence of our friends.",
               "If you can't fly, then run. If you can't run, then walk. If you can't walk, then crawl, but whatever you do, you have to keep moving.",
               "Change does not roll in on the wheels of inevitability, but comes through continuous struggle.",




]

images_list = ["https://www.uncsa.edu/chancellor/communications/img/martin-luther-king-jr.jpg",
               "https://bunny-wp-pullzone-5vqgtgkbhi.b-cdn.net/wp-content/uploads/2023/04/Civil-Rights-Leaders-in-Selma.jpg",
               "https://hips.hearstapps.com/hmg-prod/images/civil-rights-leader-martin-luther-king-waves-to-supporters-news-photo-1704903196.jpg",
               "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRLFhBvc6VHdljC0pmKz-5P-1RkM09QpWrDhg&s",
               "https://imgc.artprintimages.com/img/print/mlk-st-augustine-boycott-1964_u-l-q10ouy80.jpg?background=F3F3F3", 
               "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRnOX7EO074KbbjKIE-tIzHIrJnaOg2u5_D1g&s",
               


]

def quote(request):
  template_name = 'quotes/quote.html'
  context = {
    'quote': random.choice(quotes_list),
    'image': random.choice(images_list),
  }

  return render(request, template_name, context)

def show_all(request):
  template_name = 'quotes/show_all.html'
  context = {
    'quotes': quotes_list,
    'images': images_list,
  }

  return render(request, template_name, context)

def about(request):
  template_name= 'quotes/about.html'
  context = {
    'name': 'Martin Luther King Jr.',
    'persons_description': 'Martin Luther King Jr. was a ket civil rights activist. He was an active leader during the American Civil Rights Movement advocating for African American equal rights.\n His most notable moments were the March on Washington, Montgomery Bus Boycott and "I Have a Dream" speech.',
    'creator' : 'Emmanuel Eyob',
    'creator_description': 'I created this for a school project and I am very inspired by the movement led by Martin Luther King Jr.',
  
  }

  return render(request, template_name, context)



