import itertools
import factory
from .models import Agency
from core.factories import UserFactory
from client.factories import ClientFactory


class AgencyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Agency

    name = factory.Sequence(lambda n: f'Agency{n}')

    @factory.post_generation
    def users(obj, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            assert isinstance(extracted, int)
            for i in range(extracted):
                user = UserFactory(username=f'{obj.name}-user{i}')
                user.profile.agency = obj
                user.save()

    @factory.post_generation
    def clients(obj, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            assert isinstance(extracted, int)
            profiles_iterator = itertools.cycle(obj.user_profiles.all())
            for i in range(extracted):
                user = next(profiles_iterator).user
                client = ClientFactory(created_by=user)
                client.agency_clients.create(agency=user.profile.agency)
