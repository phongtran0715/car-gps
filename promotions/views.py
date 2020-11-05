from django.shortcuts import render
from django.utils.translation import gettext as _
from .models import Promotions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import status


# Create your views here.
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def api_get_promotion_view(request, *args, **kwargs):
	data = {}
	if Promotions.objects.filter(active=True).count() > 0:
		promotion = Promotions.objects.filter(active=True).order_by('created_at')[0]
		
		if request.is_secure():
			protocol = 'https'
		else:
			protocol = 'http'
		data ={
			"title" : promotion.title,
			"image" : protocol + '://' + request.get_host() + promotion.image.url,
			"url" : promotion.url,
			"created_at" : promotion.created_at
		}
	else:
		data = {
			'message' : _('Not found promotion')
		}
		return Response(data, status=status.HTTP_404_NOT_FOUND)
	return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_promotion_view(request, *args, **kwargs):
	context = {
		'promotions' : Promotions.objects.all()
	}

	return render(request, "promotions/promotions.html", context)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_promotion_view(request, *args, **kwargs):
	pass


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def update_promotion_view(request, *args, **kwargs):
	context = {}

	return render(request, "promotions/promotions.html", context)


@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def delete_promotion_view(request, *args, **kwargs):
	context = {}

	return render(request, "promotions/promotions.html", context)	