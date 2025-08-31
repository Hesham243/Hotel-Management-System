from django.shortcuts import render, redirect, get_object_or_404
from .models import Hotel,Room,Booking
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .forms import BookingForm
from django import forms
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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

@login_required
def rooms(request):
    rooms = Room.objects.prefetch_related('images').all()
    return render(request, 'room/index.html', {"rooms": rooms})

@login_required
def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    images = room.images.all()
    return render (request, 'room/detail.html', {'room':room, 'images':images})
    
@login_required
def booking_index(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking_index.html', {'bookings': bookings})

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'booking_detail.html', {'booking': booking})




# CBV for Booking Create

class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking/booking_form.html'
    success_url = reverse_lazy('booking-index')


    def get_initial(self):
        initial = super().get_initial()
        room_id = self.kwargs.get('room_id')
        if room_id:
            initial['room'] = room_id
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        room_id = self.kwargs.get('room_id')
        if room_id:
            form.fields['room'].widget.attrs['readonly'] = True
            form.fields['room'].widget = forms.HiddenInput()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_id = self.kwargs.get('room_id')
        if room_id:
            from .models import Room
            context['room_obj'] = Room.objects.get(pk=room_id)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)




# CBV for Booking Update

class BookingUpdateView(LoginRequiredMixin, UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking_form.html'
    success_url = reverse_lazy('booking-index')

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)




# CBV for Booking Delete

class BookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = 'booking_confirm_delete.html'
    success_url = reverse_lazy('booking-index')

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


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


    