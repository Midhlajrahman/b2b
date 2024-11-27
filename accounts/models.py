from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

class User(AbstractUser):
    agent_code = models.CharField(max_length=8, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.agent_code:
            self.agent_code = self.generate_agent_code()
        super().save(*args, **kwargs)
        self.send_agent_code_email()  

    def generate_agent_code(self):
        """Generate a unique agent code in the format AGT-XXXX."""
        while True:
            code = f"AGT-{get_random_string(4, allowed_chars='0123456789')}"
            if not User.objects.filter(agent_code=code).exists():
                return code
            
    def send_agent_code_email(self):
        """Send an email with the agent code to the user."""
        subject = "Your Agent Code"
        message = f"Hello {self.username},\n\nYour agent code is: {self.agent_code}.\nThank you for registering!"
        from_email = "secure.gedexo@gmail.com"  # Replace with your default 'from' email
        recipient_list = [self.email]
        send_mail(subject, message, from_email, recipient_list)
