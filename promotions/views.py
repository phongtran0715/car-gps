from django.utils.translation import gettext as _
from .models import Promotions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import status


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def api_get_promotion_view(request, *args, **kwargs):
	data = {}
	try:
		promotion = Promotions.objects.filter(active=True).order_by('created_at')
		if promotion.count() > 0:
			if request.is_secure():
				protocol = 'https'
			else:
				protocol = 'http'
			data ={
				"title" : promotion[0].title,
				"image" : protocol + '://' + request.get_host() + promotion[0].image.url,
				"url" : promotion[0].url,
				"created_at" : promotion[0].created_at
			}
			return Response(data, status=status.HTTP_200_OK)
		else:
			data = {
				'message' : _('Not found promotion')
			}	
			return Response(data, status=status.HTTP_404_NOT_FOUND)
	except Promotions.DoesNotExist:
		data = {
			'message' : _('Not found promotion')
		}
		return Response(data, status=status.HTTP_404_NOT_FOUND)