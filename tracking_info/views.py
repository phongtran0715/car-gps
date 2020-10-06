# Create your views here.
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
    data = {}
    if request.method == 'GET':
        info = CarTrackingInfo.objects.filter(user_id=account.id).latest('id')
        data['response'] = {
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
    data = {}
    if request.method == 'GET':
        data['response'] = "PENDING"
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
            car_info = serializer.data
            account.car_info.create(latitude=car_info['latitude'], longitude=car_info['longitude'], gas=car_info['gas'],
                                    gps_status=car_info['gps_status'], speed=car_info['speed'],
                                    odometer=car_info['odometer'], timestamp=car_info['timestamp'])
            data['response'] = "tracking information update success"
            return Response(data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
