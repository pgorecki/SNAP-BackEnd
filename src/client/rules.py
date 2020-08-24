import rules


@rules.predicate
def can_read_client(user, client):
    if user.is_superuser:
        return True

    return user == client.created_by


def can_modify_client(user, client):
    if user.is_superuser:
        return True

    return user == client.created_by


rules.add_rule('can_read_client', can_read_client)
rules.add_rule('can_modify_client', can_modify_client)
