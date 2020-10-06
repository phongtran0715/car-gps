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
    if request.method == 'GET':
        obj = CarTrackingInfo.objects.filter(user_id=account.id)
        return Response(obj)
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
        tracking_data = account.tracking_info
        data['response'] = tracking_data
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def insert_tracking_info_view(request, **kwargs):
    try:
        request.user
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CarTrackingSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        serializer.save()
        data['response'] = "tracking information update success"
        return Response(data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)