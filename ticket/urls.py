from django.urls import path
from . import views
app_name = "ticket"


urlpatterns = [
    path("checkout/<str:order_id>/",views.checkout,name="checkout"),
    path("ajax_load_ticket/",views.ajax_load_ticket,name="ajax_load_ticket"),
    
]