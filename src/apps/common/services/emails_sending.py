from typing import Any, Union

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_email(
    template_name: str,
    recipients: Union[str, list[str]],
    context: dict[str, Any] = None,
    from_email: str = None,
) -> None:
    """
    Generic email sending function that loads templates from Django templates
    and sends emails with both HTML and text versions.

    Args:
        template_name: Name of the email template (without path)
        context: Dictionary of context variables for template rendering
        recipients: Email address(es) to send to (string or list of strings)
        from_email: Sender email address (defaults to DEFAULT_FROM_EMAIL)

    Template structure expected:
        templates/emails/{template_name}/subject.txt
        templates/emails/{template_name}/body.txt
        templates/emails/{template_name}/body.html

    Example usage:
        >>> send_email(
        ...     template_name='welcome',
        ...     context={'user_name': 'John'},
        ...     recipients=[user.email],
        ... )
    """
    # Ensure recipients is a list
    if isinstance(recipients, str):
        recipients = [recipients]

    # Ensure context defaults context instead of None
    if context is None:
        context = {}

    # Extend context with built-in variables
    extended_context = {
        **context,
        "site_url": settings.SITE_URL,
        "project_name": settings.PROJECT_NAME,
    }
    template_pref = f"emails/{template_name}"

    # Render templates
    subject = render_to_string(
        f"{template_pref}/subject.txt", context=extended_context
    ).strip()
    text_content = render_to_string(
        f"{template_pref}/body.txt", context=extended_context
    )
    html_content = render_to_string(
        f"{template_pref}/body.html", context=extended_context
    )

    # Create email message
    from_email = from_email or settings.DEFAULT_FROM_EMAIL
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=recipients,
    )
    # Attach HTML message
    msg.attach_alternative(html_content, "text/html")

    # Send email
    msg.send()
