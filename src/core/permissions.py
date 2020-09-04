from rest_framework.permissions import IsAuthenticated
from cancan.ability import AbilityValidator
from cancan.middleware import CanCanMiddleware


class AbilityPermission():
    def has_permission(self, request, view=None):
        validator = request.ability
        ability = validator.ability
        ability.set_alias('list', 'view')
        ability.set_alias('retrieve', 'view')
        ability.set_alias('create', 'add')
        ability.set_alias('update', 'change')
        ability.set_alias('partial_update', 'change')
        ability.set_alias('destroy', 'delete')
        result = validator.can(view.action, view.get_queryset().model)
        return result

        return validator.can(view.action, view.get_queryset().model)

    def has_object_permission(self, request, view, obj):
        validator = request.ability
        ability = validator.ability
        ability.set_alias('list', 'view')
        ability.set_alias('retrieve', 'view')
        ability.set_alias('create', 'add')
        ability.set_alias('update', 'change')
        ability.set_alias('partial_update', 'change')
        ability.set_alias('destroy', 'delete')
        return validator.can(view.action, obj)


class IsAgencyMemberReadOnly(IsAuthenticated):
    """
    Allows access read-only to authenticated users.
    """

    def has_permission(self, request, view=None):
        if view.action not in ['list', 'retrieve']:
            return False

        try:
            return bool(request.user.profile.agency)
        except AttributeError:
            pass
        return False


class IsAgencyMember(IsAuthenticated):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view=None):
        try:
            return bool(request.user.profile.agency)
        except AttributeError:
            pass
        return False


class IsAdmin(IsAuthenticated):
    """
    Allows access only to admins.
    """

    def has_permission(self, request, view=None):
        try:
            return request.user.is_superuser
        except AttributeError:
            pass
        return False


class IsOwner(IsAuthenticated):
    """
    Checks if created_by is the same as the user
    """

    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user
