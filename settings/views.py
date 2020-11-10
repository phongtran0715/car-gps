from django.shortcuts import render
import logging
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.state import User
from .models import VinatrackSettings
from .serializers import VinatrackSettingsSerializer


# Create your views here.
# Get an instance of a logger
logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def settings_view(request, **kwargs):
	try:
		account = request.user
	except User.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		settings = VinatrackSettings.objects.get(id=account.id)
		serializer = VinatrackSettingsSerializer(settings)
		data = serializer.data
		data['user_id'] = account.id
		data['user_name'] = account.username
		data['email'] = account.email

		if request.is_secure():
			protocol = 'https'
		else:
			protocol = 'http'

		return Response(data, status=status.HTTP_200_OK)
	return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def update_settings_view(request, **kwargs):
	try:
		account = request.user
	except User.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)


	if request.method == 'PUT':
		settings = account.settings
		serializer = VinatrackSettingsSerializer(data=request.data)
		data = {}
		if serializer.is_valid():
			settings.notification = serializer.data['notification']
			settings.language = serializer.data['language']
			settings.map_display = serializer.data['map_display']
			settings.distance_unit = serializer.data['distance_unit']
			settings.datetime_format = serializer.data['datetime_format']
			settings.refresh_interval = serializer.data['refresh_interval']
			settings.theme = serializer.data['theme']

			settings.save()
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
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def reset_default_view(request, **kwarg):
	try:
		account = request.user
	except User.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'POST':
		settings = account.settings
		settings.notification = True
		settings.language = 'vi'
		settings.map_display = 'map'
		settings.distance_unit = 'km'
		settings.datetime_format = 'YYYY-MM-DD HH:mm:ss'
		settings.refresh_interval = 20
		settings.theme = 'light'
		
		settings.save()
		data['message'] = "Successful"
		return Response(data, status=status.HTTP_200_OK)
	return Response(status=status.HTTP_400_BAD_REQUEST)