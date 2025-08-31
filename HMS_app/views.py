
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Hotel,Room,Booking
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .forms import BookingForm

def home(request):
    return HttpResponse('<h1>Hello customer</h1>')

def about(request):
    return render(request, 'about.html')

def rooms(request):
    rooms = Room.objects.all()
    return render(request, 'room/index.html', {"rooms": rooms})

def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    images = room.images.all()
    return render (request, 'room/detail.html', {'room':room}, {'images':images})
    
def booking_index(request):
    bookings = Booking.objects.all()
    return render(request, 'booking_index.html', {'bookings': bookings})

def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'booking_detail.html', {'booking': booking})




# CBV for Booking Create
class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking_form.html'
    success_url = reverse_lazy('booking-index')




# CBV for Booking Update
class BookingUpdateView(UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking_form.html'
    success_url = reverse_lazy('booking-index')




# CBV for Booking Delete
class BookingDeleteView(DeleteView):
    model = Booking
    template_name = 'booking_confirm_delete.html'
    success_url = reverse_lazy('booking-index')
