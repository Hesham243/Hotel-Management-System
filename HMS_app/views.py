
from django.shortcuts import render, redirect, get_object_or_404
from .models import Hotel,Room,Booking
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .forms import BookingForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.decorators import login_required

def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'home.html', {'form': form, 'next': request.GET.get('next', '')})

def about(request):
    return render(request, 'about.html')

def rooms(request):
    rooms = Room.objects.prefetch_related('images').all()
    return render(request, 'room/index.html', {"rooms": rooms})

def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    images = room.images.all()
    return render (request, 'room/detail.html', {'room':room, 'images':images})
    
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


class Home(LoginView):
    template_name = 'home.html'
    
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)


    