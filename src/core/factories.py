import factory
from .models import User, UserProfile


# https://simpleit.rocks/python/django/setting-up-a-factory-for-one-to-many-relationships-in-factoryboy/


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: "%s@example.com" % obj.username)
    password = "password"


class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = factory.SubFactory(UserFactory)
    agency = factory.SubFactory("agency.factories.AgencyFactory")
