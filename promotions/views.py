from django.shortcuts import render
from .models import Promostions


# Create your views here.
def get_promotion_view(request):
	context = {
		'promotions' : Promostions.objects.all()
	}

	return render(request, "promotions/promotions.html", context)


def create_promotion_view(request):
	pass
	# context = {}

	# return render(request, "promotions/promotions.html", context)


def update_promotion_view(request):
	context = {}

	return render(request, "promotions/promotions.html", context)


def delete_promotion_view(request):
	context = {}

	return render(request, "promotions/promotions.html", context)	