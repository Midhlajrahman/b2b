
import uuid
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.serializers import serialize
from datetime import datetime
from django.http import JsonResponse
from decimal import Decimal
#model
from web.models import TouristDestination
from ticket.models import OrderItem,Ticket,TicketGroupPrice
#form
from web.forms import OrderForm


def ajax_load_ticket(request):
    destination = request.GET.get('destination')
    select_date = request.GET.get('select_date')
    select_date = datetime.strptime(select_date, '%m/%d/%Y').date()
    instances = Ticket.objects.filter(
        group_price__destination__pk=destination,
        validity_from_date__lte=select_date,
        validity_end_date__gte=select_date,
        status=False
    )
    instance = instances.order_by('-validity_end_date').last()

    if instance is not None:
        serialized_instance = serialize('json', [instance], use_natural_primary_keys=True)

    else:
        serialized_instance = None
    guist_count = instances.filter(group_price__age_group='adult').count()
    child_count = instances.filter(group_price__age_group='children').count()

    return JsonResponse({
        'instance': serialized_instance,
        'select_date': select_date,
        'guist_count': guist_count,
        'child_count': child_count,
        'destination': destination,
        'order_id': generate_order_id()
    })


def generate_order_id():
    timestamp = timezone.now().strftime("%y%m%d")
    unique_id = uuid.uuid4().hex[:6] 
    return f"{timestamp}{unique_id.upper()}"


@login_required
def checkout(request,order_id):

    guist_count = int(request.GET.get('guist_count', 0))
    child_count = int(request.GET.get('child_count', 0))
    select_date = request.GET.get('select_date')
    destination_id =(request.GET.get('destination'))
    destination = TouristDestination.objects.get(pk=destination_id)
    select_date_obj = datetime.strptime(select_date, '%Y-%m-%d').date()

    if request.method == 'POST':
        
        adult_count = request.POST.get('ad-count')
        child_count = request.POST.get('child-count')
        if adult_count is None:
            adult_count = 0
        if not child_count:
            child_count = 0
        child_ticket_count = None
        ad_ticket_count = None
        form = OrderForm(request.POST)
        if form.is_valid():
            adult_data = TicketGroupPrice.objects.filter(destination=destination,age_group='adult').last()
            child_data = TicketGroupPrice.objects.filter(destination=destination,age_group='children').last()
            payable_amt = 0
            if int(adult_count) > 0:
                ad_ticket_count = Ticket.objects.filter(group_price__pk=adult_data.pk, validity_end_date__gte=select_date_obj,status=False)[:int(adult_count)]
                adult_t = Decimal(adult_count) * destination.get_price().price
                payable_amt += adult_t
            if int(child_count) > 0:
                child_ticket_count = Ticket.objects.filter(group_price__pk=child_data.pk, validity_end_date__gte=select_date_obj,status=False)[:int(child_count)]
                child_t = Decimal(child_count) * destination.get_child_price().price
                payable_amt += child_t
            

            data = form.save(commit=False)
            data.order_id = order_id
            data.user = request.user
            data.payable=Decimal(payable_amt)
            data.booked_date = select_date_obj
            data.guest_adult = guist_count
            data.guest_child = child_count
            data.ordered_at = timezone.now()
            data.save()
            if ad_ticket_count :  
                for i in ad_ticket_count:
                    OrderItem.objects.create(
                        ticket=i,
                        order=data
                    )
                    Ticket.objects.filter(pk=i.pk).update(status=True)
            if child_ticket_count :
                for i in child_ticket_count:
                    OrderItem.objects.create(
                        ticket=i,
                        order=data
                    )
                    Ticket.objects.filter(pk=i.pk).update(status=True)
            payment_url = reverse('web:payment', kwargs={'pk':data.pk})
            return redirect(payment_url)
        else:
            print(form.errors)
      
    else:
        form = OrderForm(initial={'booked_date': select_date})

    context = {
        'guist_count': guist_count,
        'child_count':child_count,
        'destination': destination,
        'select_date': select_date,
        'form': form,
    }
    return render(request, "web/checkout.html", context)



