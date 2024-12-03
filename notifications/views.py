from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

# Create your views here.

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    unread = notifications.filter(is_read=False)
    for notification in unread:
        notification.is_read = True
        notification.save()
    return render(request, 'notifications/list.html', {'notifications': notifications})
