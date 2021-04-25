# Create your views here.
import datetime
import time

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.state import User

from .models import CarTrackingInfo
from tracking_info.serializers import CarTrackingSerializer
from geopy.distance import geodesic
import json
from django.core.paginator import InvalidPage
from django.shortcuts import render
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging
from django.db.models import Q


logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_live_tracking_view(request, **kwargs):
	try:
		account = request.user
	except User.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	if request.method == 'GET':
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
		distance_day = get_distance_latest_day(account.id)
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
	try:
		account = request.user
	except User.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'POST':
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
			total_distance, avg_speed , stop_time = get_trip_info(tracking_record)
			data['total_distance'] = total_distance
			data['avg_speed'] = avg_speed
			data['stop_count'] = stop_time
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
	try:
		account = request.user
	except User.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'POST':
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

		if page > paginator.num_pages or page <= 0:
			data['data'] = []
		else:
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

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def insert_tracking_info_view(request, **kwargs):
	try:
		account = request.user
	except User.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	serializer = CarTrackingSerializer(data=request.data)
	data = {}
	if request.method == 'POST':
		if serializer.is_valid():
			is_stop=False
			if len(account.car_info.all()) > 0:
				latest_info = account.car_info.latest('timestamp')
				delta_time = datetime.datetime.strptime(serializer.data['timestamp'], '%Y-%m-%dT%H:%M:%SZ') - latest_info.timestamp.replace(tzinfo=None)
				delta_time = delta_time.total_seconds()
				if delta_time > 300.0:
					is_stop = True

			new_info = account.car_info.create(latitude=serializer.data['latitude'], longitude=serializer.data['longitude'],
										gas=serializer.data['gas'], gps_status=serializer.data['gps_status'],
										odometer=serializer.data['odometer'], speed=serializer.data['speed'], is_stop=is_stop,
										timestamp=serializer.data['timestamp'])
			new_info.save()

			# distance_day = get_distance_latest_day(account.id)
			data = {
				'speed' : -1,
				'distance' : -1
			}
			return Response(data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)	
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_trip_info(tracking_record):
	distance = 0
	total_time = 0
	avg_speed = 0
	stop_times = tracking_record.filter(Q(is_stop=True)).count()
	for i in range(0, len(tracking_record) - 1):
		delta_time = (tracking_record[i+1].timestamp - tracking_record[i].timestamp).total_seconds()
		if delta_time > 0 and delta_time <=300:
			distance += geodesic((tracking_record[i].latitude, tracking_record[i].longitude), 
				(tracking_record[i+1].latitude, tracking_record[i+1].longitude)).km
			total_time += delta_time
	if delta_time != 0:
		avg_speed = (distance) / (total_time / 3600)

	return int(distance), int(avg_speed), int(stop_times)

def get_distance_latest_day(user_id):
	today = datetime.date.today()
	info = CarTrackingInfo.objects.filter(timestamp__year=today.year, timestamp__month=today.month, timestamp__day=today.day, user_id=user_id)
	distance = 0
	for i in range(0, len(info) - 1):
		distance += geodesic((info[i].latitude, info[i].longitude), 
			(info[i+1].latitude, info[i+1].longitude)).km
	return round(distance)

def index(request):
	return render(request, 'tracking_info/index.html')

@permission_classes((IsAuthenticated,))
def room(request, room_name):
	return render(request, 'tracking_info/room.html', {
		'room_name': room_name
	})