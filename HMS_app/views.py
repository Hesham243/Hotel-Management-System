from django.shortcuts import render
from django.http import HttpResponse
from .models import Hotel,Room,Booking

def home(request):
    return HttpResponse('<h1>Hello customer</h1>')

def about(request):
    return render(request, 'about.html')

def rooms(request):
    rooms = Room.objects.all()
    return render(request, 'room/index.html', {"rooms": rooms})

def room_detail(request, room_id):
    room = Room.objects.get(id=room_id)
    return render (request, 'room/detail.html', {'room':room})
    