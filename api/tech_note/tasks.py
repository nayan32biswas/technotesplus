from django_celery_beat.models import IntervalSchedule, PeriodicTask

print(IntervalSchedule.objects.filter())
print(PeriodicTask.objects.filter())