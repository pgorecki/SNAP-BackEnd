import rules


@rules.predicate
def can_read_client(user, client):
    if user.is_superuser:
        return True

    return user == client.created_by


rules.add_rule("can_read_client", can_read_client)
