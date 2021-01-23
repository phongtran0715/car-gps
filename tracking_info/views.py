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
        start_time = request.data.get('start_time')
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ')

        end_time = request.data.get('end_time')
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%SZ')

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
def insert_tracking_info_view(request, **kwargs):
    try:
        account = request.user
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CarTrackingSerializer(data=request.data)
    data = {}
    if request.method == 'POST':
        if serializer.is_valid():
            if account.car_info.all().count() > 0:
                latest_info = account.car_info.latest('timestamp')
                # Calculate speed information
                distance = geodesic((latest_info.latitude, latest_info.longitude), (serializer.data['latitude'],serializer.data['longitude'])).km
                # check distance change
                distance_m = distance * 1000
                if distance_m < 20:
                    data = {
                        'speed' : latest_info.speed,
                        'distance' : distance_m,
                        'from' : latest_info.timestamp,
                        'to' : serializer.data['timestamp']
                    }
                    return Response(data, status=status.HTTP_200_OK)

                new_info = account.car_info.create(latitude=serializer.data['latitude'], longitude=serializer.data['longitude'],
                                        gas=serializer.data['gas'], gps_status=serializer.data['gps_status'],
                                        odometer=serializer.data['odometer'],
                                        timestamp=serializer.data['timestamp'])
                
                new_time = datetime.datetime.strptime(new_info.timestamp, '%Y-%m-%dT%H:%M:%SZ')
                delta_time = new_time - latest_info.timestamp.replace(tzinfo=None)
                delta_time = delta_time.total_seconds()

                if delta_time != 0.0:
                    speed_km = (distance) / (delta_time / 3600)
                else:
                    speed_km = 0.0

                new_info.speed = round(speed_km)
                new_info.save()
                
                distance_day = get_distance_latest_day(account.id)

                data = {
                    'speed' : new_info.speed,
                    'distance' : distance_day,
                    'from' : latest_info.timestamp,
                    'to' : new_info.timestamp
                }
                # send message to admin app
                # channel_layer = get_channel_layer()
                # print("channel layer: {}".format(channel_layer))
                # async_to_sync(channel_layer.group_send)('tracking_' + account.username, {
                #     'type': 'chat_message',
                #     "message": {
                #         "latitude" : serializer.data['latitude'],
                #         "longitude" : serializer.data['longitude'],
                #         "gas" : serializer.data['gas'],
                #         "gps_status" : serializer.data['gps_status'],
                #         "odometer" : serializer.data['odometer'],
                #         "timestamp" : serializer.data['timestamp']
                #     }
                # })

                return Response(data, status=status.HTTP_200_OK)
            else:
                new_info = account.car_info.create(latitude=serializer.data['latitude'], longitude=serializer.data['longitude'],
                                        gas=serializer.data['gas'], gps_status=serializer.data['gps_status'],
                                        odometer=serializer.data['odometer'],
                                        timestamp=serializer.data['timestamp'])
                new_info.speed = 0.0
                new_info.save()
                data = {
                    'speed' : "0.0",
                    'distance' : 0,
                    'from' : serializer.data['timestamp'],
                    'to' : serializer.data['timestamp']
                }
                # send message to admin app
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)('tracking_' + account.username, {
                    'type': 'chat_message',
                    "message": {
                        "latitude" : serializer.data['latitude'],
                        "longitude" : serializer.data['longitude'],
                        "gas" : serializer.data['gas'],
                        "gps_status" : serializer.data['gps_status'],
                        "odometer" : serializer.data['odometer'],
                        "timestamp" : serializer.data['timestamp']
                    }
                })
                return Response(data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_trip_info(tracking_record):
    distance = 0
    avg_speed = 0
    stop_time = 0
    for i in range(0, len(tracking_record) - 1):
        distance += geodesic((tracking_record[i].latitude, tracking_record[i].longitude), 
            (tracking_record[i+1].latitude, tracking_record[i+1].longitude)).km
        # if location dose not change >= 5 min -> car stop
        if tracking_record[i+1].timestamp - tracking_record[i].timestamp > datetime.timedelta(minutes=5):
            stop_time += 1

    end_time = tracking_record.last().timestamp
    start_time = tracking_record.first().timestamp
    delta_time = (end_time - start_time).seconds
    if delta_time != 0:
        avg_speed = (distance) / (delta_time / 3600)

    return round(distance), round(avg_speed) , round(stop_time)

def get_distance_latest_day(user_id):
    today = datetime.date.today()
    print("Today is : {}".format(today))
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