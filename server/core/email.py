from django.apps import apps
from django.conf import settings
import sendgrid
from sendgrid.helpers.mail import Email, To, Content, Mail

from tech_note.celeryconf import app

SENDER_EMAIL = settings.SENDER_EMAIL
API_BROWSER_HOST = settings.API_BROWSER_HOST


@app.task
def send_share_email_async(share_with_id):
    ShareWith = apps.get_model(app_label="note", model_name="ShareWith")
    share = ShareWith.objects.get(id=share_with_id)

    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)

    from_email = Email(SENDER_EMAIL)
    to_email = To(share.user.email)
    subject = f"Note Share With you: {share.note.name}"

    message = f"""
    {share.note.owner.email} shared a document With you.
    visit: {API_BROWSER_HOST} # TODO: url
    """

    content = Content("text/plain", message)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    print(f"{response.status_code}\n\n{response.body}\n\n")  # {response.headers}


def send_share_email(share_with_id):
    # send_share_email_async(share_with_id)
    send_share_email_async.delay(share_with_id)
