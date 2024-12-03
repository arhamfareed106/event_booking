from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from bookings.models import Booking
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def payment_process(request):
    booking_id = request.session.get('booking_id')
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        try:
            token = request.POST.get('stripeToken')
            charge = stripe.Charge.create(
                amount=int(booking.event.price * 100),  # amount in cents
                currency='usd',
                description=f'Payment for {booking.event.title}',
                source=token,
            )
            
            # Mark booking as paid
            booking.status = 'confirmed'
            booking.save()
            
            messages.success(request, 'Payment successful!')
            return redirect('payment_success')
            
        except stripe.error.CardError as e:
            messages.error(request, f"Payment failed: {str(e)}")
            
    return render(request, 'payments/process.html', {
        'booking': booking,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })

@login_required
def payment_success(request):
    booking_id = request.session.get('booking_id')
    if booking_id:
        booking = get_object_or_404(Booking, id=booking_id)
        del request.session['booking_id']
        return render(request, 'payments/success.html', {'booking': booking})
    return redirect('home')
