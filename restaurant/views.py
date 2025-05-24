from django.shortcuts import render
import time, random

# Create your views here.

#Home page and restaurant description information
def main(request):
    template_name= 'restaurant/main.html'
    context = {
    'restaurant_description': 'We are a Boston based Ethiopian restaurant serving authentic dishes from the motherland. We stand out by our flavourful cusine along with our daily specials. We also have a live traditional music band playing every night.',
    }
    return render(request, template_name, context)

# Special items handling section
def order(request):
    template_name = 'restaurant/order.html'
    special_items = [
        'Alicha Misir',
        'Siga Wot',
        'Chechebsa',
        'Keysir',

    ]

    daily_special = random.choice(special_items)
    return render(request, template_name, {'daily_special': daily_special})

# Handles confirmation of order, extras selection on one food item, and estimated food finishing time
def confirmation(request):
      template_name = "restaurant/confirmation.html"

      if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        special_instructions = request.POST.get('special_instructions')
        daily_special = request.POST.get('daily_special')
        kitfo_extras = request.POST.getlist('kitfo_extras')

      
      menu = {
          'Kitfo': 22,
          'Tibs': 20,
          'Doro': 15,
          
      }
  
      menu[daily_special] = 30

      total = 0
      ordered = []

      for food_name, price in menu.items():
          if request.POST.get(food_name):
              ordered.append(food_name)
              total +=price
              if food_name == 'Kitfo' and kitfo_extras:
                  ordered.append("Kitfo Extras: " + ", ".join(kitfo_extras))
                  

      minutes = random.randint(30, 60)
      finish_date = time.strftime('%B %d, %Y', time.localtime(time.time() + minutes * 60))
      finish_time = time.strftime('%I:%M %p', time.localtime(time.time() + minutes * 60))

      context = {
          'name': name,
          'phone': phone,
          'email': email,
          'special_instructions': special_instructions,
          'ordered': ordered,
          'total': total,
          'finish_date': finish_date,
          'finish_time': finish_time,
      }

      return render(request, template_name, context)
      


        
    

