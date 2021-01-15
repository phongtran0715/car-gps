from .models import CarTrackingInfo
import datetime

def db_rotation_job():
	print("Delete car tracking record after 10 days")
	delete_time = datetime.datetime.strptime(datetime.now()-timedelta(days=10), '%Y-%m-%dT%H:%M:%SZ')
	record_count = CarTrackingInfo.objects.filter(timestamp__gte=delete_time).count()
	print("count : {}".format(record_count))