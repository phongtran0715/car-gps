from rest_framework import generics, status
# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.state import User

from user_profile.models import UserProfile
from user_profile.serializers import UserProfileSerializer
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def profile_view(request, **kwargs):
    try:
        account = request.user
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        profile = UserProfile.objects.get(id=account.id)
        serializer = UserProfileSerializer(profile)
        data = serializer.data
        data['avatar'] = {
            "original_image_url": "https://lorempixel.com/640/480/people/?63783",
            "thumb_image_url": "http://lorempixel.com/150/150/?63783"
        }
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def update_profile_view(request, **kwargs):
    try:
        account = request.user
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        profile = account.profile
        serializer = UserProfileSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            profile.car_name = serializer.data['car_name']
            profile.first_name = serializer.data['first_name']
            profile.last_name = serializer.data['last_name']
            profile.email = serializer.data['email']
            profile.phone = serializer.data['phone']
            profile.imei = serializer.data['imei']
            profile.plate_number = serializer.data['plate_number']
            profile.avatar = serializer.data['avatar']

            profile.save()
            data['message'] = "Successful"
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def change_avatar_view(request, **kwargs):
    try:
        request.user
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = {'avatar': {
        "original_image_url": "https://lorempixel.com/640/480/people/?63783",
        "thumb_image_url": "http://lorempixel.com/150/150/?63783"
    }}
    return Response(data, status=status.HTTP_200_OK)


def upload_image_view(request):
    if request.method == 'POST' and request.FILES['image_file']:
        myfile = request.FILES['image_file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'user_profile/upload_image.html',
            {
                'uploaded_file_url' : uploaded_file_url
            })
    return render(request, 'user_profile/upload_image.html')