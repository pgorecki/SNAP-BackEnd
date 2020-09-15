import json
from django.conf import settings
from django.http import HttpResponseNotFound
from django.views import defaults
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from agency.serializers import AgencyReader
from core.logging import logger
from survey.models import Survey, Question, Response as SurveyResponse
from client.models import Client


class HealthViewSet(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, format=None):
        data = {'status': 'up', 'build_version': settings.BUILD_VERSION, 'build_date': settings.BUILD_DATE}
        logger.info('Health check')
        return Response(data)


class UsersMe(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        permissions = set()
        for g in request.user.groups.all():
            for p in g.permissions.all():
                permissions.add(p)

        for p in request.user.user_permissions.all():
            permissions.add(p)

        perms = map(lambda p: "{}.{}".format(p.content_type.app_label, p.codename), permissions)

        content = {
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'permissions': sorted(perms),
            'is_superuser': request.user.is_superuser,
            'agency': request.user.profile and AgencyReader(request.user.profile.agency).data
        }
        return Response(content)


class DashboardSummary(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {
            'clients': request.ability.queryset_for('view', Client).distinct().count(),
            'surveys': request.ability.queryset_for('view', Survey).count(),
            'responses': request.ability.queryset_for('view', SurveyResponse).distinct().count(),
            'questions': request.ability.queryset_for('view', Question).count(),
        }
        return Response(content)


def error404(request, exception):
    if request.headers.get('Accept') == 'application/json':
        response_data = {}
        response_data['detail'] = 'Not found.'
        return HttpResponseNotFound(json.dumps(response_data), content_type="application/json")
    return defaults.page_not_found(request, exception)


def error500(request):
    if request.headers.get('Accept') == 'application/json':
        response_data = {}
        response_data['detail'] = 'Internal server error.'
        return HttpResponseNotFound(json.dumps(response_data), content_type="application/json")
    return defaults.server_error(request)
