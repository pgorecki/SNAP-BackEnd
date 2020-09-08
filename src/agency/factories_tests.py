from .factories import AgencyFactory


def test_agency_factory():
    agency = AgencyFactory(users=2)

    members = agency.user_profiles.all()
    assert len(members) == 2
