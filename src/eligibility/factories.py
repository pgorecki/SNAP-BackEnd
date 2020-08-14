import factory
from agency.factories import AgencyFactory
from .models import Eligibility, EligibilityQueue


class EligibilityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Eligibility

    name = factory.Sequence(lambda n: f'Eligibility {n}')


class EligibilityQueueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EligibilityQueue


class AgencyWithEligibilityFactory(AgencyFactory):

    @factory.post_generation
    def num_eligibility(obj, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            assert isinstance(extracted, int)
            eligibility = EligibilityFactory.create_batch(extracted)
            obj.eligibility.set(eligibility)
