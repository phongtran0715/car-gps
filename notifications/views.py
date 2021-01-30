from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Notifications
from .forms import NotificationsForm

# Create your views here.
# @api_view(['GET'])
@permission_classes((IsAuthenticated,))

def get_notification_view(request, *args, **kwargs):

	notifications = Notifications.objects.all()
	context = {
		'notifications' : notifications
	}
	return render(request, "notifications/notifications.html", context)


def notification_new(request):
    if request.method == "POST":
        form = NotificationsForm(request.POST, request.FILES)
        if form.is_valid():
            notification = form.save(commit=False)
            notification.author = request.user
            img_obj = form.instance
            notification.url = img_obj.image.url
            notification.save()
            return redirect('../../notifications')
    else:
        form = NotificationsForm()
        print("error")
    return render(request, 'notifications/notification_new.html', {'form': form})

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def api_get_notification_view(request, *args, **kwargs):
	# TODO : get notification for user
	data = {
			"body" : "The Amazing Spider-Man 2 Getting an IMAX 3D Release",
			"title" : "Spider-Man 2",
			"image" : "https://www.comingsoon.net/assets/uploads/2013/12/file_112239_0_spiderman2trailer.jpg",
			"hyperlink" : "https://www.comingsoon.net/movies/news/112239-the-amazing-spider-man-2-getting-an-imax-3d-release" 
		}
	return Response(data, status=status.HTTP_200_OK)