from django.shortcuts import render , redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from notifications.models import Notification
from discover.views import getRecs


# Create your views here
def notifications(request):
    user = request.user
    notifications = Notification.objects.filter(to_user=user)
    unread = Notification.objects.filter(to_user=user, is_read=False)
    for notification in unread:
        notification.is_read = True
        notification.save()

    return render(request, 'notifications/includes/notifications.html',
                  {'notifications': notifications})

def notifications_check(request):
    #print("check notificatios function call ...")
    user = request.user
    notifications = Notification.objects.filter(to_user=user,is_read=False)[:5]
    #print len(notifications)
    return HttpResponse(len(notifications))

def notifications_last(request):
    user = request.user
    notifications = Notification.objects.filter(to_user=user,is_read=False)[:5]
    for notification in notifications:
        #print notification
        notification.is_read = True
        notification.save()

    return render(request,
                      'notifications/includes/last_notifications.html',
                  {'notifications': notifications})
