from client.models import Client


def declare_abilities(user, ability):
    if user.has_perm('client.view_client'):
        ability.declare_can('view', Client)

    if user.has_perm('client.add_client'):
        ability.declare_can('add', Client)

    if user.has_perm('client.change_client'):
        ability.declare_can('change', Client)

    if user.has_perm('client.delete_client'):
        ability.declare_can('delete', Client)
