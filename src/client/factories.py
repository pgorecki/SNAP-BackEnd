import factory
from .models import Client


class ClientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Client

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("first_name")
    dob = factory.Faker("date_between", start_date="-60y", end_date="-20y")
