from django.urls import path
from . import views
from django.views.generic import TemplateView
from .views import CustomLoginView

app_name = "accounts"

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    ]