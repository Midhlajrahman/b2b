from django.urls import path
from . import views


app_name = "web"

urlpatterns = [

    path("", views.index, name="index"),
    path("cities/", views.cities, name="cities"),
    path("destinations/", views.destinations, name="destinations"),
    path("destination/<uuid:pk>/", views.destination, name="destination"),
    path("destination-details/<uuid:pk>/", views.destination_details, name="destination-details"),
   
    path("contact/",views.contact,name="contact"),
    path("updates-single/<slug>/", views.updates_single, name="updates-single"),
    path('search/', views.search_view, name='search'),

    path("callback/verify/", views.StripeWebhookView.as_view(), name="payment_callback"),
    path("payment/<str:pk>/", views.PaymentView.as_view(), name="payment"),
    path("orders-list/", views.OrdersList.as_view(), name="orders_list"),
    path("order/success/<str:pk>/", views.OrderSuccessView.as_view(), name="order_success"),
    path("order/failed/<str:pk>/", views.OrderFailedView.as_view(), name="order_failed"),
    path('download_tickets/<str:order_id>/',views.DownloadTicketsView.as_view(), name='download_tickets'),
    path('check-availability/', views.check_availability, name='check-availability')
]