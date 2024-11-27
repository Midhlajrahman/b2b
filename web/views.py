import json
import requests
import stripe
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.utils import timezone
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from urllib.parse import urljoin
from io import BytesIO
from PIL import Image 
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
#models
from django.db.models import Max
from web.models import  DestinationCity, PartnerLogo, TouristDestination,Testimonial,Blog,ThingsToDo,DestinationImage
from ticket.models import Ticket,Order,OrderItem,TicketGroupPrice
#forms
from web.forms import OrderForm
from .forms import ContactForm ,SearchForm 
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
import qrcode
import tempfile

@login_required
def index(request):
    # city = DestinationCity.objects.all()
    city = TouristDestination.objects.all()
    popular_destinations = TouristDestination.objects.filter(popular_destination=True)
    testimonials = Testimonial.objects.all()
    partner_logos = PartnerLogo.objects.all()
    blogs = Blog.objects.all()[:4]
    form = SearchForm(request.GET)
    # cities = list(DestinationCity.objects.values("name", "description_heading")) 
    cities = list(TouristDestination.objects.values("name")) 
    cities_json = json.dumps(list(cities)) 
    
    context = {
        "cities": city,
        "testimonials":testimonials,
        "popular_destinations":popular_destinations,
        "is_index": True,
        "blogs":blogs,
        'partner_logos':partner_logos,
        "form":form,    
        "cities_data": cities_json
    }
    return render(request, "web/index.html", context)

@login_required
def cities(request):
    city = DestinationCity.objects.all()
    context = {
        "city": city,
        "is_cities": True,
    }
    return render(request, "web/cities.html", context)

@login_required
def destinations(request):
    
    destinations = TouristDestination.objects.all()
   
    context = {
        'destinations': destinations,
        
    }
    return render(request, "web/activities.html", context)

@login_required
def destination(request, pk):
    city = DestinationCity.objects.get(pk=pk)
    testimonials = Testimonial.objects.all()
    blogs = Blog.objects.all()[:3]
    things_to_do = ThingsToDo.objects.filter(city=city)
   
    context = {
        "city": city,
        "is_destination": True,
        "testimonials": testimonials,
        "blogs":blogs,
        "things_to_do":things_to_do,
    }
    return render(request, "web/destinations.html", context)


def destination_details(request, pk):
    destination = TouristDestination.objects.get(pk=pk) 
    tickets = Ticket.objects.filter(group_price__destination=destination)
    max_validity_date = tickets.aggregate(Max('validity_end_date'))['validity_end_date__max']
   
    context = {
        "destination_detail": destination,
        "is_destination_detail": True,
        "max_validity_date": max_validity_date,
    }
    return render(request, "web/destination-details.html", context)

@login_required
def contact(request):
    form = ContactForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            response_data = {
                "status": "true",
                "title": "Successfully Submitted",
                "message": "Thank You, Our Team Will Contact you Soon",
            }
        else:
            response_data = {
                "status": "false",
                "title": "form validation error",
                "message": repr(form.errors),
            }
        return HttpResponse(
            json.dumps(response_data), content_type="application/javascript"
        )
    else:
        context = {
            "form": form,
            "is_contact": True,
        }
    return render(request, 'web/contact.html', context)

@login_required
def updates_single(request, slug):
    updates = Blog.objects.get(slug=slug)

    context = {
        "updates": updates,
        "is_updates": True,
    }
    return render(request, "web/updates-single.html", context)

@login_required
# def search_view(request):
#     city = request.GET.get('city')
#     date = request.GET.get('date')
#     form = SearchForm(request.GET)
#     results = TouristDestination.objects.all()
#     available_packages = PackageDates.objects.filter(destination__name=city, available_date=date)
#     if form.is_valid():
#         query = form.cleaned_data['query']
#         results = results.filter(name__icontains=query)
#     context = {
#         'form': form,
#         'results': results,
#         'city': city,
#         'date': date,
#         'available_packages': available_packages,  
#     }
#     return render(request, 'web/search_results.html', context)

def search_view(request):
    city = request.GET.get('city')
    date_str = request.GET.get('date')
    form = SearchForm(request.GET)
    results = TouristDestination.objects.all()

    # Parse the date input
    try:
        search_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        search_date = None

    # Filter based on city and availability within the date range
    if city and search_date:
        # Filter TicketGroupPrice by city
        group_prices = TicketGroupPrice.objects.filter(destination__name=city)
        
        # Find available tickets within the date range for each group price
        available_tickets = Ticket.objects.filter(
            group_price__in=group_prices,
            validity_from_date__lte=search_date,
            validity_end_date__gte=search_date,
            status=False  # Assuming `status=True` indicates an available ticket
        )

        # Extract unique packages (group prices) from the available tickets
        available_packages = group_prices.filter(ticket__in=available_tickets).distinct()
    else:
        available_packages = PackageDates.objects.none()  # Empty queryset if city or date is not provided

    # Search within TouristDestination if form is valid
    if form.is_valid():
        query = form.cleaned_data['query']
        results = results.filter(name__icontains=query)

    context = {
        'form': form,
        'results': results,
        'city': city,
        'date': date_str,
        'available_packages': available_packages,
    }
    return render(request, 'web/search_results.html', context)


# payment & booking
class PaymentView(DetailView):
    template_name = "web/payment.html"
    model = Order

    def post(self, request, pk, *args, **kwargs):
        order = self.get_object()
        stripe.api_key = settings.STRIPE_SECRET_KEY

        
        customer = stripe.Customer.create(
            email=order.user.email,
            name=f"{order.full_name}",
            address={
                "country": order.country,
            },
            phone=order.phone_number,
        )

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "aed",
                            "unit_amount": int(order.payable * 100),
                            "product_data": {
                                "name": "   B2B HOLIDAYS WEB CHECKOUT",
                            },
                        },
                        "quantity": 1,
                    }
                ],
                metadata={
                    "order_pk": order.pk,
                    "order_id": order.order_id,
                },
                customer=customer.id,
                mode="payment",
                success_url=request.build_absolute_uri(reverse("web:order_success", kwargs={"pk": order.pk})),
                cancel_url=request.build_absolute_uri(reverse("web:order_failed", kwargs={"pk": order.pk})),
            )
            order.is_ordered = True
            order.save()
            return redirect(checkout_session.url)
        except Exception as e:
            print(e)
            return redirect(reverse("web:order_failed", kwargs={"pk": order.pk}))

    def get(self, request, pk, *args, **kwargs):
        order = self.get_object()
        return render(request, self.template_name, {"order": order})


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(View):
    def post(self, request, format=None):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )

            if event["type"] == "checkout.session.completed":
                print("Payment successful")
                session = event["data"]["object"]
                customer_email = session["customer_details"]["email"]
                order = get_object_or_404(Order, pk=session["metadata"]["order_pk"])
                order.is_ordered = True
                order.ordered_at =  timezone.now()
                order.save()

            return HttpResponse(status=200)

        except ValueError as e:
            # Invalid payload
            details = repr(e)
            return JsonResponse({"status": 400, "message": "Invalid payload", "details": details})
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            print(e)
            details = repr(e)
            return JsonResponse({"status": 400, "message": "Invalid signature", "details": details})


class OrderSuccessView(DetailView):
    model = Order
    template_name = "web/order_success.html"

    def get_object(self):
        return get_object_or_404(Order, pk=self.kwargs["pk"])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_instance = self.get_object()
        order_instance.is_ordered = True
        order_instance.ordered_at =  timezone.now()
        order_instance.save()

        context['order_instance'] = order_instance

        return context


class OrderFailedView(DetailView):
    model = Order
    template_name = "web/order_failed.html"

    def get_object(self):
        return get_object_or_404(Order, pk=self.kwargs["pk"])


class DownloadTicketsView(View):
    def get(self, request, order_id):
        # Fetch the order and associated tickets
        order_items = OrderItem.objects.filter(order__order_id=order_id)
        tickets_data = [
            {   
                "name": item.ticket.serial_number,
                "Guest Type": f" {item.ticket.group_price.age_group}",
                "details": f" {item.ticket.validity_from_date} to {item.ticket.validity_end_date}",
                "pdf_image": item.ticket.ticket_pdf.url
            }
            for item in order_items
        ]

        # Generate PDF
        pdf_buffer = BytesIO()
        pdf = canvas.Canvas(pdf_buffer, pagesize=letter)

        for ticket in tickets_data:
            # Draw basic ticket details
            pdf.drawString(100, 750, f"Ticket: {ticket['name']}")
            pdf.drawString(100, 730, f"Guest Type: {ticket['Guest Type']}")
            pdf.drawString(100, 710, f"Validity: {ticket['details']}")

            # Generate QR code for the ticket's serial number
            qr_code = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,
                                    box_size=10, border=4)
            qr_code.add_data(ticket['name'])
            qr_code.make(fit=True)

            # Create an image from the QR code
            img = qr_code.make_image(fill='black', back_color='white')

            # Save the image to a temporary file (in PNG format)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_qr_file:
                img.save(tmp_qr_file, format='PNG')
                tmp_qr_file.close()  # File is now saved and we can use its path

                # Embed the QR code into the PDF (using the temporary file path)
                # qr_x = letter[0] 
                # qr_y = 250  
                qr_x = 400 
                qr_y = 700 
                pdf.drawImage(tmp_qr_file.name, qr_x, qr_y, width=100, height=100)

            # Ensure image URL is correct and fetch the image
            img_url = urljoin(request.build_absolute_uri(), ticket['pdf_image'])
            img_data = requests.get(img_url).content
            img_stream = BytesIO(img_data)
            img = Image.open(img_stream)

            # Save the image to a temporary file (in PNG format)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_img_file:
                img.save(tmp_img_file, format='PNG')
                tmp_img_file.close()  # File is now saved and we can use its path

                # Calculate the center position for the image horizontally
                center_x = (letter[0] - img.width) / 2

                # Embed the image into the PDF (using the temporary file path)
                pdf.drawImage(tmp_img_file.name, center_x, 350, width=img.width, height=img.height)

            pdf.showPage()

        pdf.save()

        # Create a response and set the appropriate headers
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{order_id}_tickets.pdf"'

        # Write the PDF to the response
        pdf_buffer.seek(0)
        response.write(pdf_buffer.read())

        return response

    

class OrdersList(LoginRequiredMixin,ListView):
    template_name = "web/orders_list.html"
    model = Order
    paginate_by = 50

    def get_queryset(self):
        return Order.objects.filter(is_ordered=True,user=self.request.user)


class OrderView(LoginRequiredMixin,DetailView):
    template_name = "web/order_view.html"
    model = Order
    context_object_name = "order"
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_items"] = OrderItem.objects.filter(order=self.object)
        return context
    
# def check_availability(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         city_name = data.get('city')
#         date = data.get('date')
#         print(city_name)
#         print(date)

#         try:
#             available_date = datetime.strptime(date, '%Y-%m-%d').date()
#         except ValueError:
#             return JsonResponse({'available': False, 'error': 'Invalid date format'}, status=400)
#         available = PackageDates.objects.filter(
#             desination__name=city_name,
#             available_date=available_date
#         ).exists()

#         return JsonResponse({'available': available})

# def check_availability(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         city_name = data.get('city')
#         date = data.get('date')
        
#         try:
#             available_date = datetime.strptime(date, '%Y-%m-%d').date()
#         except ValueError:
#             return JsonResponse({'available': False, 'error': 'Invalid date format'}, status=400)

     
#         ticket_group_price = TicketGroupPrice.objects.filter(
#             destination__name=city_name
#         ).first()
#         print(ticket_group_price)

#         if ticket_group_price:
          
#             ticket = Ticket.objects.filter(
#                 group_price=ticket_group_price,
#                 validity_from_date__lte=available_date,
#                 validity_end_date__gte=available_date
#             ).first()

#             if ticket:
            
#                 city = ticket_group_price.destination
#                 destination_images = DestinationImage.objects.filter(destination=city)

               
#                 city_image_url = city.image.url if city.image else ""
#                 destination_image_urls = [image.image.url for image in destination_images]

#                 return JsonResponse({
#                     'available': True,
#                     'city_image': city_image_url,
#                     'destination_images': destination_image_urls
#                 })

#         return JsonResponse({'available': False})

def check_availability(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        city_name = data.get('city')
        date = data.get('date')
        
        try:
            available_date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'available': False, 'error': 'Invalid date format'}, status=400)

        ticket_group_price = TicketGroupPrice.objects.filter(
            destination__name=city_name
        ).first()
        
        if ticket_group_price:
            ticket = Ticket.objects.filter(
                group_price=ticket_group_price,
                validity_from_date__lte=available_date,
                validity_end_date__gte=available_date
            ).first()

            if ticket:
                city = ticket_group_price.destination
                destination_images = DestinationImage.objects.filter(destination=city)
                
                # Get the first image's URL if available
                city_image_url = destination_images[0].image.url if destination_images.exists() else ""
                destination_image_urls = [image.image.url for image in destination_images]

                return JsonResponse({
                    'available': True,
                    'city_image': city_image_url,
                    'destination_images': destination_image_urls
                })

        return JsonResponse({'available': False})