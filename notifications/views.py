from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .models import Notifications
from .forms import NotificationsForm
from django.core.paginator import (Paginator, EmptyPage,
	PageNotAnInteger, InvalidPage)
from .serializers import NotificationsSerializer
import json
from fcm_django.models import FCMDevice
import logging


logger = logging.getLogger(__name__)

# Create your views here.
# @api_view(['GET'])
@permission_classes((IsAuthenticated,))

def get_notification_view(request, *args, **kwargs):

	notifications = Notifications.objects.all()
	#context = {
	#	'notifications' : notifications
	#}
	query = request.GET.get("q")
	if query:
		notifications = notifications.filter(
			title__icontains=query
		).distinct()
		paginator = Paginator(notifications, 10) # Show 25 contacts per pagepaginator = Paginator(contact_list, 25) # Show 25 contacts per page
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
  
		def next_page_number(self):
			return self.paginator.validate_number(self.number + 1)

		def previous_page_number(self):
			return self.paginator.validate_number(self.number - 1)
		return render(request, "notifications/notifications.html", {"page_obj":page_obj})
	else:    
		paginator = Paginator(notifications, 10) # Show 4 notifications per page
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)

		def next_page_number(self):
			return self.paginator.validate_number(self.number + 1)

		def previous_page_number(self):
			return self.paginator.validate_number(self.number - 1)

		return render(request, "notifications/notifications.html", {"page_obj":page_obj})

def notification_new(request):
	if request.method == "POST":
		form = NotificationsForm(request.POST, request.FILES)
		if form.is_valid():
			notification = form.save(commit=False)
			notification.author = request.user
			img_obj = form.instance
			if img_obj.image == "null":
				notification.image = ""
			else:
				notification.url = img_obj.image.url
			notification.save()
			form.save_m2m()
			# TODO: send message to specific device
			devices = FCMDevice.objects.all()
			devices.send_message(data={
					"body" : notification.body,
					"title" : notification.title,
					"image" : "https://dantri.com.vn/",
					"url" : "https://dantri.com.vn/"
			})
			return redirect('../../notifications')
	else:
		form = NotificationsForm()
		logger.error("Request method not allow")
	return render(request, 'notifications/notification_new.html', {'form': form})


def save_related(self, request, form, formsets, change):
		super().save_related(request, form, formsets, change)
		form.instance.permissions.add(request.user)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def api_get_notification_view(request, *args, **kwargs):
	try:
		account = request.user
	except User.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		page = request.data.get('page', 1)
		data = {}
		result = []
		try:
			noti_items = account.notifications.all()
		except:
			data = {
				"message": "Not found tracking data"
			}
			return Response(data, status=status.HTTP_404_NOT_FOUND)

		if noti_items.exists() == False :
			data = {
				"message": "Not found tracking data"
			}
			return Response(data, status=status.HTTP_404_NOT_FOUND)
		else:
			paginator = Paginator(noti_items, 10)
			try:
				data['total_record'] = paginator.count
				data['page'] = page
				data['total_page'] = paginator.num_pages
				data['page_size'] = 10
				if page > paginator.num_pages or page <= 0:
					data['data'] = []
				else:
					page_data = paginator.page(page)
					for item in page_data:
						serializer = NotificationsSerializer(item)
						item_data = serializer.data 
						if request.is_secure():
							protocol = 'https'
						else:
							protocol = 'http'
						if item_data['image'] is not None:
							item_data['image'] = protocol + '://' + request.get_host() + item_data['image']
						item_data['url'] = item_data['url']
						result.append(item_data)
					data['data'] = result
			except PageNotAnInteger:
				data['data'] = paginator.page(1)
			except EmptyPage:
				data['data'] = paginator.page(paginator.num_pages)
			except InvalidPage:
				data = {
					"message": "Invalid page"
				}
				return Response(data, status=status.HTTP_404_NOT_FOUND)
		return Response(data, status=status.HTTP_200_OK)
	else:
		return Response(status=status.HTTP_400_BAD_REQUEST)

def htmlspecialchars(text):
	return (
		text.replace("&", "&amp;").
		replace('"', "&quot;").
		replace("<", "&lt;").
		replace(">", "&gt;")
	)