from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

TEMPLATES = {
    "soon": "events/event_soon.html",
    "invite": "events/invite.html",
}


def send_email(
    action,
    event,
    invite=None,
):
    """Function for send email with html template."""
    context = {
        "app_label": settings.APP_LABEL,
    }
    html = get_template(TEMPLATES[action])
    context["event"] = event.name
    emails_to = [user.email for user in event.members.all()]
    if invite is not None:
        emails_to = [invite.user.email]
    html_content = html.render(context)
    msg = EmailMultiAlternatives(
        from_email=settings.EMAIL_HOST_USER,
        to=emails_to,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
