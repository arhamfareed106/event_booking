from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    capacity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def available_seats(self):
        booked_seats = self.booking_set.filter(status='confirmed').count()
        return max(0, self.capacity - booked_seats)

    def is_full(self):
        return self.available_seats() == 0

    def capacity_percentage(self):
        if self.capacity == 0:
            return 100
        booked = self.capacity - self.available_seats()
        return int((booked / self.capacity) * 100)

    def is_upcoming(self):
        return self.date >= timezone.now()

    def is_past(self):
        return self.date < timezone.now()

    def get_status(self):
        if not self.is_active:
            return 'Cancelled'
        if self.is_past():
            return 'Past'
        if self.is_full():
            return 'Sold Out'
        return 'Available'

    class Meta:
        ordering = ['date']

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booking_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.event.price * Decimal(self.quantity)
        super().save(*args, **kwargs)

    def can_cancel(self):
        return (
            self.status == 'confirmed' and 
            self.event.date > timezone.now() and
            (self.event.date - timezone.now()).days >= 1
        )

    def get_status_display_color(self):
        status_colors = {
            'pending': 'yellow',
            'confirmed': 'green',
            'cancelled': 'red'
        }
        return status_colors.get(self.status, 'gray')

    class Meta:
        ordering = ['-booking_date']
        unique_together = ['user', 'event']
