from django.shortcuts import render
from .models import Toy

def home(request):
    toys = Toy.objects.all()
    return render(request, 'home.html', {'toys': toys})



