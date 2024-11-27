from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

class CustomLoginForm(AuthenticationForm):
    agent_code = forms.CharField(max_length=8, required=True, label=_("Agent Code"))

    def clean(self):
        # Get form data
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        agent_code = self.cleaned_data.get('agent_code')

        # Authenticate the user using username and password
        user = authenticate(username=username, password=password)

        # If authentication is successful, check the agent_code
        if user is not None:
            if user.agent_code != agent_code:
                # If the agent_code doesn't match, raise an error
                raise forms.ValidationError(_("Invalid agent code."), code='invalid_agent_code')
        else:
            # If authentication failed, raise an error
            raise forms.ValidationError(_("Invalid username or password."), code='invalid_login')

        # Return the cleaned data if everything is valid
        return self.cleaned_data
