from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Event, Booking
from django.utils import timezone

def home(request):
    featured_events = Event.objects.filter(
        is_active=True,
        date__gte=timezone.now()
    ).order_by('date')[:6]
    return render(request, 'bookings/home.html', {
        'events': featured_events,
    })

def event_list(request):
    events_list = Event.objects.filter(
        is_active=True,
        date__gte=timezone.now()
    ).order_by('date')
    
    paginator = Paginator(events_list, 9)  # Show 9 events per page
    page = request.GET.get('page')
    events = paginator.get_page(page)
    
    return render(request, 'bookings/event_list.html', {
        'events': events,
        'is_paginated': events.has_other_pages(),
        'page_obj': events,
    })

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    user_has_booking = False
    if request.user.is_authenticated:
        user_has_booking = Booking.objects.filter(
            user=request.user,
            event=event,
            status='confirmed'
        ).exists()
    
    return render(request, 'bookings/event_detail.html', {
        'event': event,
        'user_has_booking': user_has_booking,
    })

@login_required
def dashboard(request):
    upcoming_bookings = request.user.booking_set.filter(
        event__date__gte=timezone.now(),
        status='confirmed'
    ).order_by('event__date')
    past_bookings = request.user.booking_set.filter(
        event__date__lt=timezone.now(),
        status='confirmed'
    ).order_by('-event__date')
    
    return render(request, 'bookings/dashboard.html', {
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings,
    })

@login_required
def booking_list(request):
    upcoming_bookings = request.user.booking_set.filter(
        event__date__gte=timezone.now()
    ).order_by('event__date')
    past_bookings = request.user.booking_set.filter(
        event__date__lt=timezone.now()
    ).order_by('-event__date')
    
    return render(request, 'bookings/booking_list.html', {
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings,
    })

@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'bookings/booking_detail.html', {
        'booking': booking,
    })

@login_required
def create_booking(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    
    # Check if user already has a booking
    existing_booking = Booking.objects.filter(
        user=request.user,
        event=event,
        status__in=['pending', 'confirmed']
    ).first()
    
    if existing_booking:
        messages.error(request, 'You already have a booking for this event.')
        return redirect('event_detail', pk=event_id)
    
    # Check if event is full
    if event.is_full():
        messages.error(request, 'Sorry, this event is fully booked.')
        return redirect('event_detail', pk=event_id)
    
    if request.method == 'POST':
        booking = Booking.objects.create(
            user=request.user,
            event=event,
            status='pending'
        )
        messages.success(request, 'Booking created successfully!')
        return redirect('booking_detail', pk=booking.pk)
    
    return render(request, 'bookings/create_booking.html', {
        'event': event,
    })

@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        if booking.can_cancel():
            booking.status = 'cancelled'
            booking.save()
            messages.success(request, 'Booking cancelled successfully.')
            return redirect('booking_list')
        else:
            messages.error(request, 'This booking cannot be cancelled.')
    return render(request, 'bookings/cancel_booking.html', {
        'booking': booking,
    })
