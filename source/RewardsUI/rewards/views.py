import logging
import requests

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView


class RewardsView(TemplateView):
    """Default view for the rewards UI."""
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__)):
        super(RewardsView, self).__init__()
        self.logger = logger

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        order_email = request.POST.get('order_email')
        order_total = request.POST.get('order_total')
        customer_email = request.POST.get('customer_email')

        requests.post(
            "http://rewardsservice:7050/order",
            data={
                "email": order_email,
                "total": order_total})

        context['rewards_data'] = RewardsView.__get_rewards__()

        context['customer_email'] = customer_email
        context['customer_data'] = RewardsView.__get_customers__(
            customer_email)

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        customer_email = request.GET.get('customer_email', None)

        context['rewards_data'] = RewardsView.__get_rewards__()

        context['customer_email'] = customer_email
        context['customer_data'] = RewardsView.__get_customers__(
            customer_email)

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    @staticmethod
    def __get_rewards__():
        response = requests.get("http://rewardsservice:7050/rewards")
        return response.json()

    @staticmethod
    def __get_customers__(customer_email=""):
        customer_data = None
        if customer_email is None or customer_email is '':
            # Empty email field, return all customers.
            response = requests.post("http://rewardsservice:7050/customer",
                                     data={"email": None})
            customer_data = response.json()
        else:
            # Single response, wrap the JSON in an array.
            response = requests.post("http://rewardsservice:7050/customer",
                                     data={"email": customer_email})
            try:
                if response.json()["error"] is not None:
                    customer_data = [response.json()]
            except KeyError:
                customer_data = [response.json()]
            except TypeError:
                customer_data = None

        return customer_data
