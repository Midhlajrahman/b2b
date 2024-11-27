from django.dispatch import receiver
from registration.signals import user_activated
from django.core.mail import send_mail
from .models import User

@receiver(user_activated)
def send_agent_code_after_activation(sender, user, request, **kwargs):
    # Check if the user has an agent code; generate if missing
    if not user.agent_code:
        user.agent_code = user.generate_agent_code()
        user.save() 

    # Send email with the agent code
    subject = "Your Agent Code"
    message = f"Hello {user.username},\n\nYour agent code is: {user.agent_code}.\nThank you for activating your account!"
    from_email = "secure@gedexo.com"  # Replace with your 'from' email
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)