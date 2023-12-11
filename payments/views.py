import json

import stripe
from django.conf import settings  # new
from django.http.response import JsonResponse, HttpResponse  # new
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt  # new
from django.views.generic.base import TemplateView
from datetime import datetime

from citas.models import Cita


class HomePageView(TemplateView):
    template_name = 'pay.html'


class SuccessView(TemplateView):
    template_name = 'success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve query parameters from the URL
        checkout_session_id = self.request.GET.get('session_id')
        ident_string = self.request.GET.get('ident')
        now = datetime.now()  # current date and time
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

        # Convert 'ident' from string to list
        ident_list = json.loads(ident_string)

        for ident in ident_list:
            try:
                # Perform actions using the ident value
                # Fetch the Cita object and update the properties based on the ident value if needed
                cita = Cita.objects.get(id=ident)
                cita.pagado = True
                cita.check_pago = "PAGO CORRECTO || " + date_time + " || ID=" + checkout_session_id
                cita.save()
            except Exception as e:
                print(f"Error processing ident: {str(e)}")

        # Add parameters to the context to pass them to the template
        context['checkout_session_id'] = checkout_session_id
        context['ident'] = ident_list

        return context


class CancelledView(TemplateView):
    template_name = 'cancelled.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve query parameters from the URL
        checkout_session_id = self.request.GET.get('session_id')
        ident_string = self.request.GET.get('ident')
        now = datetime.now()  # current date and time
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

        # Convert 'ident' from string to list
        ident_list = json.loads(ident_string)

        for ident in ident_list:
            try:
                # Perform actions using the ident value
                # Fetch the Cita object and update the properties based on the ident value if needed
                cita = Cita.objects.get(id=ident)
                cita.pagado = False
                cita.check_pago = "PAGO CANCELADO O NO CORRECTO || " + date_time + " || ID=" + checkout_session_id
                cita.save()
            except Exception as e:
                print(f"Error processing ident: {str(e)}")

        # Add parameters to the context to pass them to the template
        context['checkout_session_id'] = checkout_session_id
        context['ident'] = ident_list

        return context


# new
@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        domain_url = 'http://localhost:8000/checkout/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'price': 'price_1OK0pIEuWVOCbA5vVAl6Rlah',
                        'quantity': 1,
                    },
                    {
                        'price': 'price_1OK0hPEuWVOCbA5vyjXlc39P',
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@csrf_exempt
def create_custom_checkout_session(request):
    if request.method == 'POST':
        print(request.body)
        data = json.loads(request.body)
        priceIds = data['priceIds']
        citasIds = data['citasIds']
        domain_url = 'http://localhost:8000/checkout/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            items = []
            for i in range(len(priceIds)):
                line_item = {
                    'price': priceIds[i],
                    'quantity': 1,
                }
                items.append(line_item)
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}&ident=' + str(citasIds),
                cancel_url=domain_url + 'cancelled?session_id={CHECKOUT_SESSION_ID}&ident=' + str(citasIds),
                payment_method_types=['card'],
                mode='payment',
                line_items=items
            )
            json_response = JsonResponse({'ident': citasIds, 'sessionId': checkout_session['id']})
            print(json_response)
            print("Bien json")
            return json_response
        except Exception as e:
            json_response = JsonResponse({'ident': citasIds, 'error': str(e)})
            print(json_response)
            print("Mal json")
            return json_response


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")


    else:
        try:
            print("Bien no payment")
            ident = json_response.json().get('ident')
            if ident:
                print("Bien ident no payment")
                # Perform actions using the ident value
                # Fetch the Cita object and update the properties based on the ident value if needed
                # For example:
                cita = Cita.objects.get(id=ident)
                cita.pagado = False
                cita.check_pago = json_response
                cita.save()
            else:
                print("Ident not found in JSON response")
        except Exception as e:
            print(f"Error processing ident: {str(e)}")

    return HttpResponse(status=200)