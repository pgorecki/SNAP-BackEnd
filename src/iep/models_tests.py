from django.core.exceptions import ValidationError
from agency.factories import AgencyFactory
from client.models import Client
from program.factories import ProgramFactory, EnrollmentFactory
from eligibility.enums import EligibilityStatus
from eligibility.models import EligibilityQueue, Eligibility
from .choices import IEPStatus
from .factories import ClientIEPFactory, ClientIEPEnrollmentFactory


def test_ClientIEPEnrollment_and_Enrollment_must_have_same_client():
    agency = AgencyFactory(users=1, clients=2)
    program = ProgramFactory(agency=agency)
    client1 = Client.objects.first()
    client2 = Client.objects.last()

    assert client1.id != client2.id

    iep = ClientIEPFactory(client=client1)
    enrollment = EnrollmentFactory(client=client2, program=program)

    iep_enrollment = ClientIEPEnrollmentFactory(iep=iep, enrollment=enrollment)

    try:
        iep_enrollment.clean()
        assert False
    except ValidationError:
        pass


def test_iep_enrollment_programs_must_be_from_same_agency():
    agency1 = AgencyFactory(users=1, clients=2)
    agency2 = AgencyFactory()
    program1 = ProgramFactory(agency=agency1)
    program2 = ProgramFactory(agency=agency2)
    client = Client.objects.first()

    iep = ClientIEPFactory(client=client)
    enrollment1 = EnrollmentFactory(client=client, program=program1)
    enrollment2 = EnrollmentFactory(client=client, program=program2)

    ClientIEPEnrollmentFactory(iep=iep, enrollment=enrollment1)
    ClientIEPEnrollmentFactory(iep=iep, enrollment=enrollment2)

    try:
        iep.clean()
        assert False
    except ValidationError:
        pass


def test_iep_status_change_will_update_client_is_new_field():
    agency1 = AgencyFactory(users=1, clients=2)
    agency2 = AgencyFactory()
    program1 = ProgramFactory(agency=agency1)
    program2 = ProgramFactory(agency=agency2)
    client = Client.objects.first()

    iep = ClientIEPFactory(client=client)

    assert client.is_new is True

    iep.status = IEPStatus.IN_PROGRESS
    iep.save()

    assert client.is_new is False

    iep.status = IEPStatus.ENDED
    iep.save()

    assert client.is_new is True


def test_approving_eligibility_request_will_change_status():
    agency = AgencyFactory(users=1, clients=2)
    program = ProgramFactory(agency=agency)
    client = Client.objects.first()

    iep = ClientIEPFactory(client=client)

    Eligibility.objects.create(name='test')
    eligibility_request = EligibilityQueue.objects.create(client=client, requestor=agency)
    iep.eligibility_request = eligibility_request
    iep.save()

    iep.eligibility_request.status = EligibilityStatus.ELIGIBLE.name
    iep.eligibility_request.save()

    iep.refresh_from_db()
    assert iep.status == IEPStatus.IN_ORIENTATION


def test_denying_eligibility_request_will_change_status():
    agency = AgencyFactory(users=1, clients=2)
    program = ProgramFactory(agency=agency)
    client = Client.objects.first()

    iep = ClientIEPFactory(client=client)

    Eligibility.objects.create(name='test')
    eligibility_request = EligibilityQueue.objects.create(client=client, requestor=agency)
    iep.eligibility_request = eligibility_request
    iep.save()

    iep.eligibility_request.status = EligibilityStatus.NOT_ELIGIBLE.name
    iep.eligibility_request.save()

    iep.refresh_from_db()
    assert iep.status == IEPStatus.NOT_ELIGIBLE
