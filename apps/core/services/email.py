from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

TEMPLATES = {
    "soon": "events/event_soon.html",
}


def send_email(
    action,
    event,
):
    """Function for send email with html template."""
    context = {
        "app_label": settings.APP_LABEL,
    }
    html = get_template(TEMPLATES[action])
    context["event"] = event.name
    html_content = html.render(context)
    msg = EmailMultiAlternatives(
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email for user in event.members.all()],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
