import factory
from .models import ClientIEP, ClientIEPEnrollment


class ClientIEPFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ClientIEP


class ClientIEPEnrollmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ClientIEPEnrollment
