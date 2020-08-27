from rest_framework.permissions import IsAuthenticated
from ability.ability import Ability
from backend.ability import declare_abilities


class UserPermission():
    def has_permission(self, request, view=None):
        ability = Ability(request.user)
        declare_abilities(request.user, ability)
        actions_map = {
            'list': 'view',
            'retrieve': 'view',
            'create': 'add',
            'update': 'change',
            'partial_update': 'change',
            'destroy': 'delete'
        }
        return ability.can(action=actions_map[view.action], model=view.get_queryset().model)

    def has_object_permission(self, request, view, obj):
        ability = Ability(request.user)
        declare_abilities(request.user, ability)
        actions_map = {
            'list': 'view',
            'retrieve': 'view',
            'create': 'add',
            'update': 'change',
            'partial_update': 'change',
            'destroy': 'delete'
        }
        return ability.can(action=actions_map[view.action], model=view.get_queryset().model, instance=obj)


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
