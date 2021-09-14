from django.apps import apps
from django.conf import settings
from django.utils import timezone
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from tech_note.celeryconf import app
from core.email import send_share_email


def create_scheduler():
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=settings.RESEND_NOTIFICATION_DURATION,
        period=IntervalSchedule.HOURS,
    )
    print(f"IntervalSchedule: <{schedule}>, created: {created}")

    task_name = "Share Note Notification."
    task = "core.tasks.start_notification_scheduler"
    try:
        period, created = PeriodicTask.objects.get_or_create(
            interval=schedule, name=task_name, task=task
        )
        print(f"PeriodicTask: <{period}>, created: {created}")
    except Exception:
        PeriodicTask.objects.filter(name=task_name, task=task).update(interval=schedule)
        print("Task updated")


@app.task
def start_notification_scheduler():
    ShareWith = apps.get_model(app_label="note", model_name="ShareWith")
    depreciation_time = timezone.now() + settings.NOTE_SHARE_NOTIFICATION_AGE
    # share_after = timezone.now() + settings.RESEND_NOTIFICATION_DURATION
    share_ids = ShareWith.objects.filter(
        shared_at__lte=depreciation_time, view=0
    ).values_list("id", flat=True)
    for share_id in share_ids:
        send_share_email(share_id)
