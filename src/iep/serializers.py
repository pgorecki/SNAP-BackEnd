from rest_framework import serializers
from rest_framework.utils import model_meta
from core.serializers import ObjectSerializer, CreatedByReader, UserReader
from core.exceptions import ApplicationValidationError
from client.serializers import ClientReader
from program.models import Enrollment
from program.enums import EnrollmentStatus
from eligibility.models import ClientEligibility
from .models import ClientIEP, ClientIEPEnrollment, JobPlacement


class ClientIEPEnrollmentReader(ObjectSerializer):
    id = serializers.SerializerMethodField()
    object = serializers.SerializerMethodField()
    program = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_id(self, obj):
        return str(obj.enrollment.id)

    def get_object(self, obj):
        return obj.enrollment._meta.object_name

    def get_program(self, obj):
        return str(obj.enrollment.program.id)

    def get_status(self, obj):
        return obj.enrollment.status

    class Meta:
        model = Enrollment
        fields = ('id', 'object', 'program', 'status')


class ClientIEPEnrollmentWriter(ObjectSerializer):
    id = serializers.UUIDField()

    class Meta:
        model = Enrollment
        fields = ('id', 'status', 'client', 'program')


class JobPlacementReader(serializers.ModelSerializer):
    class Meta:
        model = JobPlacement
        fields = ('id', 'effective_date', 'hire_date', 'weekly_hours',
                  'hourly_wage', 'total_weekly_income', 'total_monthly_income',
                  'how_was_job_placement_verified', 'Company', )


class JobPlacementWriter(serializers.ModelSerializer):
    class Meta:
        model = JobPlacement
        fields = ('effective_date', 'hire_date', 'weekly_hours',
                  'hourly_wage', 'total_weekly_income', 'total_monthly_income',
                  'how_was_job_placement_verified', 'Company', )


class ClientIEPReader(ObjectSerializer):
    created_by = CreatedByReader()
    client = ClientReader()
    enrollments = ClientIEPEnrollmentReader(many=True, source='iep_enrollments')
    client_is_eligible = serializers.SerializerMethodField()
    resolved_by = serializers.SerializerMethodField()
    job_placement = JobPlacementReader(required=False)

    def get_resolved_by(self, obj):
        user = None
        if obj.eligibility_request:
            user = obj.eligibility_request.resolved_by

        return UserReader(instance=user).data if user else None

    class Meta:
        model = ClientIEP
        fields = ('id', 'object', 'client', 'orientation_completed', 'status',
                  'resolved_by', 'client_is_eligible',
                  'enrollments', 'start_date', 'end_date', 'projected_end_date',
                  'outcome', 'job_placement', 'created_by', 'created_at', 'modified_at')

    def get_client_is_eligible(self, object) -> bool:
        return ClientEligibility.is_eligible(object.client)


class ClientIEPWriter(ObjectSerializer):
    enrollments = ClientIEPEnrollmentWriter(many=True, required=False)
    job_placement = JobPlacementWriter(required=False)

    class Meta:
        model = ClientIEP
        fields = ('client', 'orientation_completed', 'status',
                  'enrollments', 'start_date', 'end_date', 'projected_end_date',
                  'outcome', 'job_placement')

    def update(self, instance, validated_data):
        if 'enrollments' in validated_data:
            iep_enrollments_to_remove = set()
            existing_programs = set()
            for iep_enrollment in instance.iep_enrollments.all():
                iep_enrollments_to_remove.add(iep_enrollment.id)
                existing_programs.add(iep_enrollment.enrollment.program)

            enrollment_data = validated_data['enrollments']

            for row in enrollment_data:
                if 'id' not in row:
                    # do not allow to modify client
                    if 'client' in row:
                        del row['client']
                    # create new enrollment
                    enrollment = Enrollment.objects.create(
                        client=instance.client,
                        **row
                    )
                    instance.iep_enrollments.create(enrollment=enrollment)
                else:
                    try:
                        iep_enrollment = instance.iep_enrollments.get(enrollment__id=row['id'])
                        enrollment = iep_enrollment.enrollment
                        del row['id']
                        iep_enrollments_to_remove.remove(iep_enrollment.id)
                        for attr, value in row.items():
                            setattr(enrollment, attr, value)
                        enrollment.save()
                    except ClientIEPEnrollment.DoesNotExist:
                        raise ApplicationValidationError({'enrollment.id': 'Not found'})

            first_invalid = instance.iep_enrollments.filter(
                id__in=iep_enrollments_to_remove,
                enrollment__status__in=[
                    EnrollmentStatus.ENROLLED.name,
                    EnrollmentStatus.COMPLETED.name,
                    EnrollmentStatus.EXITED.name
                ],
            ).first()
            if first_invalid:
                raise ApplicationValidationError({f'enrollment.[{first_invalid.id}]': 'Cannot be deleted from IEP'})

            instance.iep_enrollments.filter(id__in=iep_enrollments_to_remove).delete()

        info = model_meta.get_field_info(instance)
        for attr, value in validated_data.items():
            if attr == 'job_placement':
                if instance.job_placement:
                    JobPlacementWriter().update(instance.job_placement, value)
                else:
                    instance.job_placement = JobPlacementWriter().create(value)
            elif attr in info.relations and info.relations[attr].to_many:
                pass
            else:
                setattr(instance, attr, value)

        instance.save()

        return instance
