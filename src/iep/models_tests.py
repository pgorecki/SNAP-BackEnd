from django.core.exceptions import ValidationError
from agency.factories import AgencyFactory
from client.models import Client
from program.factories import ProgramFactory, EnrollmentFactory
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

# def test_iep_enrollments_must_be_unique():
#     agency = AgencyFactory(users=1, clients=1)
#     client = Client.objects.first()
#     program = ProgramFactory(agency=agency)
#     iep = ClientIEPFactory(client=client)
#     enrollment = EnrollmentFactory(client=client, program=program)
#     iep_enrollment1 = ClientIEPEnrollmentFactory(iep=iep, enrollment=enrollment)
#     iep_enrollment2 = ClientIEPEnrollmentFactory(iep=iep, enrollment=enrollment)

#     assert iep.iep_enrollments.count() == 2

#     try:
#         iep.clean()
#         assert False
#     except ValidationError:
#         pass
