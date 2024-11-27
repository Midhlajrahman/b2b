from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login

from .models import User

from registration.backends.default.views import CustomLoginForm
class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'registration/login.html' 

    def form_valid(self, form):
        """If the form is valid, log the user in."""
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, return form with errors."""
        return self.render_to_response(self.get_context_data(form=form))
