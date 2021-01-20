from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Notification


# Create your views here.
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_notification_view(request, *args, **kwargs):
	context = {
		'notifications' : Notifications.objects.all()
	}

	return render(request, "notifications/notifications.html", context)