from django.shortcuts import render
import random

# Create your views here.

def main(request):
    template_name= 'restaurant/main.html'
    return render(request, template_name)

def order(request):
    template_name = 'restaurant/order.html'
    menu = [
        "Kitfo",
        "Tibs",
        "Doro Wat",
        "Beyeaynetu",

    ]

    daily_special = random.choice(menu)
    return render(request, template_name, {'daily_special': daily_special})

