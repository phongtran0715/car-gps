from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Notifications
from .forms import NotificationsForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
# @api_view(['GET'])
@permission_classes((IsAuthenticated,))

def get_notification_view(request, *args, **kwargs):

    notifications = Notifications.objects.all()
    #context = {
    #	'notifications' : notifications
    #}
    query = request.GET.get("q")
    if query:
        notifications = notifications.filter(
            title__icontains=query
        ).distinct()
        paginator = Paginator(notifications, 10) # Show 25 contacts per pagepaginator = Paginator(contact_list, 25) # Show 25 contacts per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
  
        def next_page_number(self):
            return self.paginator.validate_number(self.number + 1)

        def previous_page_number(self):
            return self.paginator.validate_number(self.number - 1)
        return render(request, "notifications/notifications.html", {"page_obj":page_obj})
    else:    
	    paginator = Paginator(notifications, 10) # Show 4 notifications per page
	    page_number = request.GET.get('page')
	    page_obj = paginator.get_page(page_number)

	    def next_page_number(self):
	        return self.paginator.validate_number(self.number + 1)

	    def previous_page_number(self):
	        return self.paginator.validate_number(self.number - 1)

	    return render(request, "notifications/notifications.html", {"page_obj":page_obj})
		#return render(request, "notifications/notifications.html", context)

def notification_new(request):
    if request.method == "POST":
        form = NotificationsForm(request.POST, request.FILES)
        if form.is_valid():
            notification = form.save(commit=False)
            notification.author = request.user
            img_obj = form.instance
            if img_obj.image == "null":
                notification.image = ""
            else:
                notification.url = img_obj.image.url
            notification.save()
            form.save_m2m()
            return redirect('../../notifications')
    else:
        form = NotificationsForm()
        print("error")
    return render(request, 'notifications/notification_new.html', {'form': form})


def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.permissions.add(request.user)

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

def htmlspecialchars(text):
    return (
        text.replace("&", "&amp;").
        replace('"', "&quot;").
        replace("<", "&lt;").
        replace(">", "&gt;")
    )