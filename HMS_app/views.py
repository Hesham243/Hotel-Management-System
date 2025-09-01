import datetime
from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Hotel,Room,Booking,Profile,Services
from .forms import BookingForm, ProfileForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages





# Sign-in view for login
def sign_in(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/sign-in.html', {'form': form, 'next': request.GET.get('next', '')})

def services(request):
    services = Services.objects.all()
    return render(request, 'services.html', {'services': services})


def sevices_detail(request, service_id):
    service = get_object_or_404(Services, id=service_id)
    return render(request, 'service_detail.html', {'service': service})

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

@login_required(login_url='sign-in')
def rooms(request):
    today = datetime.date.today()
    rooms = Room.objects.prefetch_related('images').all()
    room_list = []
    for room in rooms:
        # Count confirmed bookings for this room for today or future
        booked_count = room.bookings.filter(status='confirmed', check_out_date__gt=today).count()
        available = room.total - booked_count
        room_list.append({
            'obj': room,
            'available': available
        })
    return render(request, 'room/index.html', {"rooms": room_list})

@login_required(login_url='sign-in')
def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    images = room.images.all()
    return render (request, 'room/detail.html', {'room':room, 'images':images})
    

@login_required(login_url='sign-in')
def booking_index(request):
    cancelled = False
    # Handle cancellation
    if request.method == 'POST':
        booking_id = request.POST.get('cancel_booking_id')
        if booking_id:
            booking = Booking.objects.filter(id=booking_id, user=request.user, status='confirmed').first()
            if booking:
                booking.status = 'cancelled'
                booking.save()
                cancelled = True
    bookings = Booking.objects.filter(user=request.user)
    total_count = bookings.count()
    confirmed_count = bookings.filter(status='confirmed').count()
    cancelled_count = bookings.filter(status='cancelled').count()
    return render(request, 'booking/booking_index.html', {
        'bookings': bookings,
        'cancelled': cancelled,
        'total_count': total_count,
        'confirmed_count': confirmed_count,
        'cancelled_count': cancelled_count,
    })

@login_required(login_url='sign-in')
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'booking/booking_detail.html', {'booking': booking})




# CBV for Booking Create

class BookingCreateView(LoginRequiredMixin, CreateView):
    login_url = 'sign-in'
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
            context['room_obj'] = Room.objects.get(pk=room_id)
        # Add booking summary if POST and form is bound
        form = context.get('form')
        if self.request.method == 'POST' and form and form.is_bound and form.is_valid():
            check_in = form.cleaned_data.get('check_in_date')
            check_out = form.cleaned_data.get('check_out_date')
            room = form.cleaned_data.get('room')
            if check_in and check_out and room:
                nights = (check_out - check_in).days
                if nights > 0:
                    context['total_nights'] = nights
                    context['total_price'] = nights * room.price
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = 'confirmed'
        nights = (form.instance.check_out_date - form.instance.check_in_date).days
        form.instance.total_amount = nights * form.instance.room.price
        try:
            form.instance.full_clean()
        except Exception as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)
        return super().form_valid(form)




# CBV for Booking Update

class BookingUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'sign-in'
    model = Booking
    form_class = BookingForm
    template_name = 'booking/booking_form.html'
    success_url = reverse_lazy('booking-index')

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def form_valid(self, form):
        nights = (form.instance.check_out_date - form.instance.check_in_date).days
        form.instance.total_amount = nights * form.instance.room.price
        try:
            form.instance.full_clean()
        except Exception as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)
        return super().form_valid(form)




# CBV for Booking Delete

class BookingDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'sign-in'
    model = Booking
    template_name = 'booking/booking_confirm_delete.html'
    success_url = reverse_lazy('booking-index')

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


class Home(LoginView):
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        if 'next' in request.GET:
            messages.info(request, 'Please log in to access this page.')
        return super().get(request, *args, **kwargs)
    
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            auth_login(request, user)
            return redirect('complete-profile')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

def complete_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.customer)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileForm(instance=request.user.customer)
        error_message = 'Invalid profile - try again'
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/profile_form.html', context)


class ProfileView(LoginRequiredMixin, forms.ModelForm):
    login_url = 'sign-in'
    model = Profile
    form_class = ProfileForm
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

@login_required(login_url='sign-in')
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'registration/profile.html', {'profile': profile, 'form': form})

@login_required(login_url='sign-in')
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'registration/profile_form.html', {'form': form})




    