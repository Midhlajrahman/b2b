import stripe
from django.conf import settings 
stripe.api_key = settings.STRIPE_SECRET_KEY




# myapp/views.py

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@csrf_exempt
@require_POST
def create_payment(request):

    try:
        # Create a PaymentIntent with the order amount and currency
        amount = request.POST.get('total')
        
        # You can import the Stripe SDK and set the API key as you did in Flask
        print("amoun",amount)
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='aed',
            automatic_payment_methods={
                'enabled': True,
            },
        )

        return JsonResponse({'clientSecret': intent.client_secret})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=403)
