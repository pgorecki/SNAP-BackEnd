# import factory
# import factory.django
from django.contrib.auth.models import User
from client.models import Client
from agency.models import Agency, AgencyClient


# class AgencyFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model: Agency


# class ClientFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Client

#     first_name = "John"
#     last_name = "Doe"
#     dob = "2000-01-01"
#     agency_client = factory.SubFactory(AgencyClient)


def setup_2_agencies():
    agency1 = Agency.objects.create(name='Agency 1')
    agency2 = Agency.objects.create(name='Agency 2')
    user1 = User.objects.create(username='user1', password='password')
    user1.profile.agency = agency1
    user1.save()
    user2 = User.objects.create(username='user2', password='password')
    user2.profile.agency = agency2
    user2.save()

    client1 = Client.objects.create(first_name='John', last_name='Doe',
                                    dob='2000-01-01', created_by=user1)
    client2 = Client.objects.create(first_name='Bill', last_name='Smith',
                                    dob='1999-01-01', created_by=user2)

    AgencyClient.objects.create(client=client1, agency=agency1)
    AgencyClient.objects.create(client=client2, agency=agency2)

    return (agency1, agency2, user1, user2, client1, client2)
