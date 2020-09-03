from client.models import Client, ClientAddress
from eligibility.models import EligibilityQueue
from iep.models import ClientIEP, ClientIEPEnrollment
from note.models import Note
from program.models import Enrollment
from survey.models import Survey, Question, Response


def declare_abilities(user, ability):
    """
    add, view should work on per-agency level
    change, delete should work on created_by level

    ***add - should work on any level
    ***view - should work on agency level
    ***view_all - should work on global level
    ***change_agency - should work on agency level
    ***change_all - should work on a global level
    ***delete_agency - should work on agency level
    ***delete_all - should work on a global level

    i.e.
    client.add_client    - should allow to add client
    client.view_client   - should allow to view all client accessible to agency member
    client.change_client - should allow to change own client
    client.delete_client - should allow to delete client created by the user


    expected permissions:
    "permissions": [
        "client.add_client",
        "client.change_client",
        "client.change_client_agency",
        "client.change_client_all",
        "client.delete_client",
        "client.delete_client_agency",
        "client.delete_client_all",
        "client.view_client",
        "client.view_client_agency",
        "client.view_client_all"
    ],

    """
    if not user.is_authenticated:
        return

    agency = user.profile.agency
    agency_users = [p.user for p in agency.user_profiles.all()]

    if user.has_perm('client.add_client'):
        ability.can('add', Client)
        ability.can('add', ClientAddress)

    if user.has_perm('client.view_client'):
        ability.can('view', Client, created_by=user)
        ability.can('view', ClientAddress, client__created_by=user)

    if user.has_perm('client.view_client_agency'):
        ability.can('view', Client, agency_clients__agency=agency)
        ability.can('view', ClientAddress, client__agency_clients__agency=agency)

    if user.has_perm('client.view_client_all') or user.is_superuser:
        ability.can('view', Client)
        ability.can('view', ClientAddress)

    if user.has_perm('client.change_client'):
        ability.can('change', Client, created_by=user)
        ability.can('change', ClientAddress, client__created_by=user)

    if user.has_perm('client.change_client_agency'):
        ability.can('change', Client, agency_clients__agency=agency)
        ability.can('change', ClientAddress, client__agency_clients__agency=agency)

    if user.has_perm('client.change_client_all') or user.is_superuser:
        ability.can('change', Client)
        ability.can('change', ClientAddress)

    if user.has_perm('client.delete_client'):
        ability.can('delete', Client, created_by=user)
        ability.can('delete', ClientAddress, client__created_by=user)

    if user.has_perm('client.delete_client_agency'):
        ability.can('delete', Client, created_by=user)
        ability.can('delete', ClientAddress, agency_clients__agency=agency)

    if user.has_perm('client.delete_client_all') or user.is_superuser:
        ability.can('delete', Client, agency_clients__agency=agency)
        ability.can('delete', ClientAddress, client__agency_clients__agency=agency)

    # # eligiblity queue
    # ability.can('add', EligibilityQueue)
    # ability.can('view', EligibilityQueue, client__agency_clients__agency=agency)
    # ability.can('delete', EligibilityQueue, created_by=user)

    # # iep
    # ability.can('add', ClientIEP)
    # ability.can('view', ClientIEP, client__agency_clients__agency=agency)
    # ability.can('delete', ClientIEP, created_by=user)

    # ability.can('add', ClientIEPEnrollment)
    # ability.can('view', ClientIEPEnrollment, iep__client__agency_clients__agency=agency)
    # ability.can('delete', ClientIEPEnrollment, created_by=user)

    # # note
    # ability.can('add', Note)
    # ability.can('view', Note, created_by__in=agency_users)
    # ability.can('change', Note, created_by=user)
    # ability.can('delete', Note, created_by=user)

    # # program
    # ability.can('add', Enrollment)
    # ability.can('view', Enrollment, client__agency_clients__agency=agency)
    # ability.can('change', Enrollment, created_by=user)
    # ability.can('delete', Enrollment, created_by=user)

    # # survey
    # ability.can('add', Survey)
    # ability.can('view', Survey, is_public=True)
    # ability.can('view', Survey, created_by__in=agency_users)
    # ability.can('delete', Survey, created_by=user)

    # ability.can('add', Question)
    # ability.can('view', Question, is_public=True)
    # ability.can('view', Question, created_by__in=agency_users)
    # ability.can('delete', Question, created_by=user)

    # ability.can('add', Response)
    # ability.can('view', Response, client__agency_clients__agency=agency)
    # ability.can('delete', Response, created_by=user)
