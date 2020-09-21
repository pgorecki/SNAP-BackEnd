from django.core.management.base import BaseCommand  # , CommandError
from agency.models import Agency
from agency.factories import AgencyFactory
from client.factories import ClientFactory
from survey.factories import SurveyFactory, QuestionFactory


class Command(BaseCommand):
    help = "Generates fake data"

    def add_arguments(self, parser):
        # parser.add_argument('poll_ids', nargs='+', type=int)
        pass

    def handle(self, *args, **options):
        # arguments: options['poll_ids']:
        AgencyFactory.reset_sequence(Agency.objects.count())

        self.create_agency()

    def create_agency(self):
        agency = AgencyFactory(users=2)
        for p in agency.user_profiles.all():
            ClientFactory.create_batch(5, created_by=p.user)
            SurveyFactory.create(is_public=True, created_by=p.user)
            SurveyFactory.create(is_public=False, created_by=p.user)
            QuestionFactory.create(is_public=True, created_by=p.user)
            QuestionFactory.create(is_public=False, created_by=p.user)
