from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .models import Notifications
from django.core.paginator import (Paginator, EmptyPage,
	PageNotAnInteger, InvalidPage)
from .serializers import NotificationsSerializer

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def api_get_notification_view(request, *args, **kwargs):
	if request.method == 'GET':
		page = request.data.get('page', 1)
		data = {}
		result = []
		try:
			noti_items = Notifications.objects.all()
		except Notifications.DoesNotExist:
			data = {
				"message": "Not found tracking data"
			}
			return Response(data, status=status.HTTP_404_NOT_FOUND)

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