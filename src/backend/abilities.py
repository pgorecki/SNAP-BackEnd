from client.models import Client


def declare_abilities(user, ability):
    # if user.has_perm('client.view_client_for_agency'):
    if user.is_authenticated:
        ability.can('view', Client, agency_clients__agency=user.profile.agency)
        ability.can('change', Client, created_by=user)

    if user.has_perm('client.view_client'):
        ability.can('view', Client)

    if user.has_perm('client.add_client'):
        ability.can('add', Client)

    if user.has_perm('client.change_client'):
        ability.can('change', Client)

    if user.has_perm('client.delete_client'):
        ability.can('delete', Client)
