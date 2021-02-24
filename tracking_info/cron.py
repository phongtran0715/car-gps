from .models import CarTrackingInfo
import datetime
import logging


logger = logging.getLogger(__name__)
def db_rotation_job():
    tnow = datetime.datetime.now()
    logger.info("Start cron job to delete tracking info at : {}".format(tnow))
    delete_time = datetime.datetime.strptime(str(datetime.datetime.now() - datetime.timedelta(days=60)), '%Y-%m-%d %H:%M:%S.%f')

    record = CarTrackingInfo.objects.filter(timestamp__lte=delete_time)
    record_count = CarTrackingInfo.objects.filter(timestamp__lte=delete_time).count()
    logger.info("Number expire tracking info record : {}".format(record_count))

    record_ids = record.values_list('id', flat=True)

    for i in record_ids:
        CarTrackingInfo.objects.filter(id=i).delete()

    tnow = datetime.datetime.now()
    logger.info("Finish cron job at : {}".format(tnow))
