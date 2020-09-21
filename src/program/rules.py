import rules


@rules.predicate
def can_read_program(user, program):
    if user.is_superuser:
        return True
    if user.profile.agency is None:
        return False
    return user.profile.agency.programs.filter(pk=program.id).exists()


rules.add_rule("can_read_program", can_read_program)
