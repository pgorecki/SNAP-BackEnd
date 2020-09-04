from django.contrib.auth.models import Permission, AnonymousUser
from cancan.middleware import CanCanMiddleware


class FakeRequest():
    def __init__(self):
        self.user = AnonymousUser()


def create_fake_request(user):
    request = FakeRequest()
    request.user = user
    CanCanMiddleware().process_request(request)
    return request
