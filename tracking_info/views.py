import datetime
import time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.state import User

from .models import CarTrackingInfo
from .serializers import CarTrackingSerializer
from geopy.distance import geodesic
import json
from django.core.paginator import InvalidPage
from django.shortcuts import render
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging
from django.db.models import Q, Sum


logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_live_tracking_view(request, **kwargs):
	if request.method == 'GET':
		try:
			account = request.user
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		try:
			info = CarTrackingInfo.objects.filter(user_id=account.id).latest('id')
		except CarTrackingInfo.DoesNotExist:
			data = {
				"message": "Not found tracking data"
			}
			return Response(data, status=status.HTTP_404_NOT_FOUND)
		if info.speed is None:
			info.speed = 0

		# calculate delta timestamp
		distance_day = get_distance_latest_day(account.id, info.timestamp)
		data = {
			"latitude": info.latitude,
			"longitude": info.longitude,
			"gas": -1,
			"gps_status": info.gps_status,
			"speed": info.speed,
			"odometer": distance_day,
			"timestamp": info.timestamp
		}
		return Response(data, status=status.HTTP_200_OK)
	return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def get_history_tracking_view(request, **kwargs):
	if request.method == 'POST':
		try:
			account = request.user
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		page = request.data.get('page', 1)
		start_time = datetime.datetime.strptime(request.data.get('start_time'), '%Y-%m-%dT%H:%M:%SZ')
		end_time = datetime.datetime.strptime(request.data.get('end_time'), '%Y-%m-%dT%H:%M:%SZ')

		data = {}
		result = []
		try:
			tracking_record = account.car_info.filter(timestamp__gte=start_time, timestamp__lte=end_time)
		except CarTrackingInfo.DoesNotExist:
			data = {
				"message": "Not found tracking data"
			}
			return Response(data, status=status.HTTP_404_NOT_FOUND)

		if tracking_record.exists() == False :
			data = {
				"message": "Not found tracking data"
			}
			return Response(data, status=status.HTTP_404_NOT_FOUND)

		paginator = Paginator(tracking_record, 100)
		try:
			data['total_record'] = paginator.count
			data['page'] = page
			data['total_page'] = paginator.num_pages
			data['page_size'] = 100

			stop_times = tracking_record.filter(Q(is_stop=True)).count()
			distance = tracking_record.aggregate(Sum('distance'))['distance__sum']
			avg_speed = (distance / tracking_record.count())

			data['total_distance'] = int(distance) / 1000
			data['avg_speed'] = int(avg_speed)
			data['stop_count'] = int(stop_times)
			data['first_record'] = {
				'latitude' : tracking_record.first().latitude,
				'longitude' : tracking_record.first().longitude,
				'timestamp' : tracking_record.first().timestamp,
			}
			data['last_record'] = {
				'latitude' : tracking_record.last().latitude,
				'longitude' : tracking_record.last().longitude,
				'timestamp' : tracking_record.last().timestamp,
			}

			if page > paginator.num_pages or page <= 0:
				data['data'] = []
			else:
				page_data = paginator.page(page)
				for item in page_data:
					serializer = CarTrackingSerializer(item)
					result.append(serializer.data)
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
	return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def get_history_stop_view(request, **kwargs):
	if request.method == 'POST':
		try:
			account = request.user
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		page = request.data.get('page', 1)
		start_time = datetime.datetime.strptime(request.data.get('start_time'), '%Y-%m-%dT%H:%M:%SZ')
		end_time = datetime.datetime.strptime(request.data.get('end_time'), '%Y-%m-%dT%H:%M:%SZ')

		data = {}
		result = []
		try:
			tracking_record = account.car_info.filter(timestamp__gte=start_time, timestamp__lte=end_time, is_stop=True)
		except CarTrackingInfo.DoesNotExist:
			data = {
				"message": "Not found tracking data"
			}
			return Response(data, status=status.HTTP_404_NOT_FOUND)
		if tracking_record.exists() == False :
			data = {
				"message": "Not found tracking data"
			}
			return Response(data, status=status.HTTP_404_NOT_FOUND)

		paginator = Paginator(tracking_record, 10)
		try:
			data['total_record'] = paginator.count
			data['page'] = page
			data['total_page'] = paginator.num_pages
			data['page_size'] = 10

			page_data = paginator.page(page)
			for item in page_data:
				duration = (CarTrackingInfo.objects.get(id=item.id).timestamp - CarTrackingInfo.objects.get(id=item.id -1).timestamp).total_seconds()
				result.append({
					"longitude" : CarTrackingInfo.objects.get(id=item.id -1).longitude,
					"latitude" : CarTrackingInfo.objects.get(id=item.id -1).latitude,
					"date_from" : CarTrackingInfo.objects.get(id=item.id -1).timestamp,
					"date_to" : CarTrackingInfo.objects.get(id=item.id).timestamp,
					"duration" : int(duration / 60)
					})
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

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def insert_tracking_info_view(request, **kwargs):
	if request.method == 'POST':
		try:
			account = request.user
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		request_data = request.data
		request_data["speed"] = round(request_data["speed"], 2)
		request_data["distance"] = round(request_data["speed"], 2)
		serializer = CarTrackingSerializer(data=request.data)
		data = {}
		if serializer.is_valid():
			is_stop=False
			try:
				latest_info = account.car_info.latest('timestamp')
			except CarTrackingInfo.DoesNotExist:
				latest_info = None
			
			if latest_info is not None:
				delta_time = datetime.datetime.strptime(serializer.data['timestamp'], '%Y-%m-%dT%H:%M:%SZ') - latest_info.timestamp.replace(tzinfo=None)
				delta_time = delta_time.total_seconds()
				if delta_time > 300.0:
					is_stop = True

			new_info = account.car_info.create(latitude=serializer.data['latitude'], longitude=serializer.data['longitude'],
										gas=serializer.data['gas'], gps_status=serializer.data['gps_status'],
										distance=serializer.data['distance'],
										odometer=serializer.data['odometer'], speed=serializer.data['speed'], is_stop=is_stop,
										timestamp=serializer.data['timestamp'])
			new_info.save()
			distance_day = get_distance_latest_day(account.id, datetime.datetime.strptime(serializer.data['timestamp'], '%Y-%m-%dT%H:%M:%SZ'))
			data = {
				'distance' : distance_day
			}
			return Response(data, status=status.HTTP_200_OK)
		else:
			logger.error(serializer.errors)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)	
	else:
		logger.error("Invalid request method: {}".format(request.method))
		return Response(status=status.HTTP_400_BAD_REQUEST)

def get_distance_latest_day(user_id, timestamp):
	distance = 0
	try:
		info = CarTrackingInfo.objects.filter(timestamp__year=timestamp.year,
			timestamp__month=timestamp.month, timestamp__day=timestamp.day, user_id=user_id)
		distance = info.aggregate(Sum('distance'))['distance__sum']
	except CarTrackingInfo.DoesNotExist:
		distance =0
	return round(distance/1000, 2)

def index(request):
	return render(request, 'tracking_info/index.html')

@permission_classes((IsAuthenticated,))
def room(request, room_name):
	return render(request, 'tracking_info/room.html', {
		'room_name': room_name
	})