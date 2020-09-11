import rules


@rules.predicate
def can_read_eligibility(user, eligibility):
    if user.is_superuser:
        return True
    if user.profile.agency is None:
        return False
    return user.profile.agency.agencyeligibilityconfig_set.filter(eligibility=eligibility).exists()


rules.add_rule('can_read_eligibility', can_read_eligibility)
