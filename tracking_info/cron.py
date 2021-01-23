from .models import CarTrackingInfo
import datetime

def db_rotation_job():
    print("-------------------------------")
    tnow = datetime.datetime.now()
    print(tnow)

    print("Delete car tracking record after 60 days")
    delete_time = datetime.datetime.strptime(str(datetime.datetime.now() - datetime.timedelta(days=60)), '%Y-%m-%d %H:%M:%S.%f')

    record = CarTrackingInfo.objects.filter(timestamp__lte=delete_time)
    record_count = CarTrackingInfo.objects.filter(timestamp__lte=delete_time).count()
    print("count : {}".format(record_count))

    record_ids = record.values_list('id', flat=True)

    for i in record_ids:
        print(i)
        CarTrackingInfo.objects.filter(id=i).delete()

    t = CarTrackingInfo.objects.all().count()
    print(t)
