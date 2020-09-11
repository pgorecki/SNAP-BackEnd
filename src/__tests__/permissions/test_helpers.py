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


def create_view(view_cls, action, user, user_permission=None):
    if user_permission:
        user.user_permissions.add(Permission.objects.get(codename=user_permission))
    request = create_fake_request(user)
    view = view_cls()
    view.action = action
    view.request = request
    return view
