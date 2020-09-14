from client.models import Client, ClientAddress
from eligibility.models import EligibilityQueue
from iep.models import ClientIEP, ClientIEPEnrollment
from note.models import Note
from eligibility.models import ClientEligibility, EligibilityQueue
from program.models import Enrollment, Program, EnrollmentService, EnrollmentServiceType
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
    # agency_users = [p.user for p in agency.user_profiles.all()] if agency else []

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

    # client eligibility
    if user.has_perm('eligibility.add_clienteligibility'):
        ability.can('add', ClientEligibility)

    if user.has_perm('eligibility.view_clienteligibility'):
        ability.can('view', ClientEligibility, client__created_by__in=[])

        if user.has_perm('client.view_client'):
            ability.can('view', ClientEligibility, client__created_by=user)

        if user.has_perm('client.view_client_agency'):
            ability.can('view', ClientEligibility, client__agency_clients__agency=agency)

        if user.has_perm('client.view_client_all'):
            ability.can('view', ClientEligibility)

    if user.has_perm('eligibility.change_clienteligibility'):
        if user.has_perm('client.view_client'):
            ability.can('change', ClientEligibility, client__created_by=user)

        if user.has_perm('client.view_client_agency'):
            ability.can('change', ClientEligibility, client__agency_clients__agency=agency)

        if user.has_perm('client.view_client_all'):
            ability.can('change', ClientEligibility)

    # eligibility queue
    if user.has_perm('eligibility.add_eligibilityqueue'):
        ability.can('add', EligibilityQueue)

    if user.has_perm('eligibility.view_eligibilityqueue'):
        ability.can('view', EligibilityQueue, client__created_by__in=[])

        if user.has_perm('client.view_client'):
            ability.can('view', EligibilityQueue, client__created_by=user)

        if user.has_perm('client.view_client_agency'):
            ability.can('view', EligibilityQueue, client__agency_clients__agency=agency)

        if user.has_perm('client.view_client_all'):
            ability.can('view', EligibilityQueue)

    if user.has_perm('eligibility.change_eligibilityqueue'):
        if user.has_perm('client.view_client'):
            ability.can('change', EligibilityQueue, client__created_by=user)

        if user.has_perm('client.view_client_agency'):
            ability.can('change', EligibilityQueue, client__agency_clients__agency=agency)

        if user.has_perm('client.view_client_all'):
            ability.can('change', EligibilityQueue)

    # client IEP
    if user.has_perm('iep.add_clientiep'):
        ability.can('add', ClientIEP)

    if user.has_perm('iep.view_clientiep'):
        ability.can('view', ClientIEP, client__created_by__in=[])

        if user.has_perm('client.view_client'):
            ability.can('view', ClientIEP, client__created_by=user)

        if user.has_perm('client.view_client_agency'):
            ability.can('view', ClientIEP, client__agency_clients__agency=agency)

        if user.has_perm('client.view_client_all'):
            ability.can('view', ClientIEP)

    if user.has_perm('iep.change_clientiep'):
        if user.has_perm('client.view_client'):
            ability.can('change', ClientIEP, client__created_by=user)

        if user.has_perm('client.view_client_agency'):
            ability.can('change', ClientIEP, client__agency_clients__agency=agency)

        if user.has_perm('client.view_client_all'):
            ability.can('change', ClientIEP)

    if user.has_perm('iep.delete_clientiep'):
        if user.has_perm('client.view_client'):
            ability.can('delete', ClientIEP, client__created_by=user)

        if user.has_perm('client.view_client_agency'):
            ability.can('delete', ClientIEP, client__agency_clients__agency=agency)

        if user.has_perm('client.view_client_all'):
            ability.can('delete', ClientIEP)

    # note
    if user.has_perm('note.add_note'):
        ability.can('add', Note)

    if user.has_perm('note.view_note'):
        ability.can('view', Note, created_by__profile__agency=agency)

    if user.has_perm('note.change_note'):
        ability.can('change', Note, created_by__profile__agency=agency)

    # program enrollment
    if user.has_perm('program.add_enrollment'):
        ability.can('add', Enrollment)

    if user.has_perm('program.view_enrollment'):
        ability.can('view', Enrollment, client__created_by__in=[])
        if user.has_perm('client.view_client'):
            ability.can('view', Enrollment, client__created_by=user)

        if user.has_perm('client.view_client_agency'):
            ability.can('view', Enrollment, client__agency_clients__agency=agency)

        if user.has_perm('client.view_client_all'):
            ability.can('view', Enrollment)

    if user.has_perm('program.change_enrollment'):
        ability.can('change', Enrollment, client__created_by__in=[])
        if user.has_perm('client.view_client'):
            ability.can('change', Enrollment, client__created_by=user)

        if user.has_perm('client.view_client_agency'):
            ability.can('change', Enrollment, client__agency_clients__agency=agency)

        if user.has_perm('client.view_client_all'):
            ability.can('change', Enrollment)

    # program
    if user.has_perm('program.add_program'):
        ability.can('add', Program)

    ability.can('view', Program, agency=agency)
    if user.is_superuser:
        ability.can('view', Program)

    if user.has_perm('program.add_program'):
        ability.can('add', Program)

    if user.has_perm('program.change_program'):
        ability.can('change', Program, agency=agency)
        if user.is_superuser:
            ability.can('change', Program)

    if user.has_perm('program.delete_program'):
        ability.can('delete', Program, agency=agency)
        if user.is_superuser:
            ability.can('delete', Program)

    # survey
    if user.has_perm('survey.add_survey'):
        ability.can('add', Survey)

    ability.can('view', Survey, created_by__profile__agency=agency)
    ability.can('view', Survey, is_public=True)

    if user.has_perm('survey.change_survey'):
        ability.can('change', Survey, created_by__profile__agency=agency)

    if user.has_perm('survey.delete_survey'):
        ability.can('delete', Survey, created_by__profile__agency=agency)

    # question
    if user.has_perm('survey.add_question'):
        ability.can('add', Question)

    ability.can('view', Question, created_by__profile__agency=agency)
    ability.can('view', Question, is_public=True)

    if user.has_perm('survey.change_question'):
        ability.can('change', Question, created_by__profile__agency=agency)

    if user.has_perm('survey.delete_question'):
        ability.can('delete', Question, created_by__profile__agency=agency)

    # response
    if user.has_perm('survey.add_response'):
        ability.can('add', Response)

    if user.has_perm('survey.view_response'):
        ability.can('view', Response, client__created_by__in=[])
        if user.has_perm('client.view_client'):
            ability.can('view', Response, client__created_by=user)

        if user.has_perm('client.view_client_agency'):
            ability.can('view', Response, client__agency_clients__agency=agency)

        if user.has_perm('client.view_client_all'):
            ability.can('view', Response)

    if user.has_perm('survey.change_response'):
        ability.can('change', Response, client__created_by__in=[])
        if user.has_perm('client.view_client'):
            ability.can('change', Response, client__created_by=user)

        if user.has_perm('client.view_client_agency'):
            ability.can('change', Response, client__agency_clients__agency=agency)

        if user.has_perm('client.view_client_all'):
            ability.can('change', Response)

    if user.has_perm('program.add_enrollmentservice'):
        ability.can('add', EnrollmentService)

    if user.has_perm('program.view_enrollmentservice'):
        ability.can('view', EnrollmentService, enrollment__client__created_by__in=[])
        if user.has_perm('client.view_client'):
            ability.can('view', EnrollmentService, enrollment__client__created_by=user)

        if user.has_perm('client.view_client_agency'):
            ability.can('view', EnrollmentService, enrollment__client__agency_clients__agency=agency)

        if user.has_perm('client.view_client_all'):
            ability.can('view', EnrollmentService)

    if user.has_perm('program.change_enrollmentservice'):
        ability.can('view', EnrollmentService, enrollment__client__created_by__in=[])
        if user.has_perm('client.view_client'):
            ability.can('change', EnrollmentService, enrollment__client__created_by=user)

        if user.has_perm('client.view_client_agency'):
            ability.can('change', EnrollmentService, enrollment__client__agency_clients__agency=agency)

        if user.has_perm('client.view_client_all'):
            ability.can('change', EnrollmentService)

    # enrollment service types - dictionary data
    ability.can('view', EnrollmentServiceType, agency=agency)

    # Done!
    print('gained abilities\n', "\n".join([str(x) for x in ability.abilities]), '\n for permissions',
          [x.codename for x in user.user_permissions.all()]
          )
