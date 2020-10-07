# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.state import User

from tracking_info.models import CarTrackingInfo
from tracking_info.serializers import CarTrackingSerializer


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_live_tracking_view(request, **kwargs):
    try:
        account = request.user
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        info = CarTrackingInfo.objects.filter(user_id=account.id).latest('id')
        data = {
            "latitude": info.latitude,
            "longitude": info.longitude,
            "gas": info.gas,
            "gps_status": info.gps_status,
            "speed": info.speed,
            "odometer": info.odometer,
            "timestamp": info.timestamp
        }
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_history_tracking_view(request, **kwargs):
    try:
        account = request.user
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        page = request.GET.get('page', 1)
        data = {}
        result = []
        paginator = Paginator(account.car_info.all(), 2)
        try:
            data['total'] = paginator.count
            data['page'] = page
            data['page_size'] = 2

            page_data = paginator.page(page)
            for item in page_data:
                serializer = CarTrackingSerializer(item)
                result.append(serializer.data)
            data['data'] = result
        except PageNotAnInteger:
            data['data'] = paginator.page(1)
        except EmptyPage:
            data['data'] = paginator.page(paginator.num_pages)

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
            account.car_info.create(latitude=serializer.data['latitude'], longitude=serializer.data['longitude'],
                                    gas=serializer.data['gas'], gps_status=serializer.data['gps_status'],
                                    speed=serializer.data['speed'], odometer=serializer.data['odometer'],
                                    timestamp=serializer.data['timestamp'])
            account.save()
            data['message'] = "Successful"
            return Response(data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
