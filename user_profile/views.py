from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.state import User
from .models import UserProfile
from .serializers import UserProfileSerializer
from django.core.files.storage import FileSystemStorage
import os
import uuid
import logging
from django.utils.translation import gettext as _


logger = logging.getLogger(__name__)

def generate_filename(filename):
	ext = filename.split('.')[-1]
	return '{}.{}'.format(uuid.uuid1(), ext)

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
		data['user_id'] = account.id
		data['user_name'] = account.username
		data['first_name'] = account.first_name
		data['last_name'] = account.last_name
		data['email'] = account.email

		if request.is_secure():
			protocol = 'https'
		else:
			protocol = 'http'
		data['avatar'] = {
			"original_image_url": protocol + '://' + request.get_host() + data['avatar'],
			"thumb_image_url": protocol + '://' + request.get_host() + data['avatar']
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
			account.first_name = request.data['first_name']
			account.last_name = request.data['last_name']

			account.profile.car_name = serializer.data['car_name']
			account.profile.plate_number = serializer.data['plate_number']

			account.save()
			data['message'] = "Successful"
			return Response(data, status=status.HTTP_200_OK)
		errors = []
		for it in serializer.errors:
			errors.append({
				'message' : serializer.errors[it][0],
				'code' : serializer.errors[it][0].code,
				'field': it
		})
		data = {
			"message": _("Validation errors in your request"),
			"errors": errors
		}
		return Response(data, status=status.HTTP_400_BAD_REQUEST)
	return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def change_avatar_view(request, **kwargs):
	try:
		account = request.user
	except User.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'POST':
		profile = account.profile
		avatar = request .FILES['avatar']
		fs = FileSystemStorage()
		avatar_file = fs.save(generate_filename(avatar.name), avatar)

		try:
			old_avatar = os.path.join(fs.location, str(profile.avatar))
			if os.path.isfile(old_avatar):
				os.remove(old_avatar) 
		except OSError as error: 
			logger.error(error)
		
		profile.avatar = avatar_file
		profile.save()

	if request.is_secure():
		protocol = 'https'
	else:
		protocol = 'http'
	data = {'avatar': {
		"original_image_url": protocol + '://' + request.get_host() + '/media/' + avatar_file,
		"thumb_image_url": protocol + '://' + request.get_host() + '/media/' + avatar_file
	}}
	return Response(data, status=status.HTTP_200_OK)