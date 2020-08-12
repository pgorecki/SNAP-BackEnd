"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include, handler404, handler500
from django.contrib import admin
from django.urls import path, re_path
from rest_framework import permissions
from rest_framework_nested import routers
from rest_framework.authtoken.views import obtain_auth_token
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
import core.views
import client.viewsets
import survey.viewsets
import eligibility.viewsets
import program.viewsets
import note.viewsets
import matching.viewsets
from core.logging import logger

schema_view = get_schema_view(
    openapi.Info(
        title="GEORGIA API",
        default_version='v1',
        #   description="Test description",
        #   terms_of_service="https://www.google.com/policies/terms/",
        #   contact=openapi.Contact(email="contact@snippets.local"),
        #   license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register('clients', client.viewsets.ClientViewset, basename='client')
router.register('notes', note.viewsets.NoteViewset, basename='note')
router.register('surveys', survey.viewsets.SurveyViewset, basename='survey')
router.register('questions', survey.viewsets.QuestionViewset, basename='question')
router.register('responses', survey.viewsets.ResponseViewset, basename='response')

router.register('eligibility/agency_configs', eligibility.viewsets.AgencyEligibilityConfigViewset,
                basename='agency_eligibility_config')
router.register('eligibility/clients', eligibility.viewsets.ClientEligibilityViewset,
                basename='eligibility_clients')
router.register('eligibility/queue', eligibility.viewsets.EligibilityQueueViewset,
                basename='eligibility_queue')
router.register('eligibility', eligibility.viewsets.EligibilityViewset,
                basename='eligibility')
router.register('programs/enrollments', program.viewsets.EnrollmentViewset,
                basename='enrollment')
router.register('programs/eligibility', program.viewsets.ProgramEligibilityViewset,
                basename='eligibility')
router.register('programs', program.viewsets.ProgramViewset, basename='program')
router.register('matching/config', matching.viewsets.MatchingConfigViewset, basename='matching_config')

router.register('matching', matching.viewsets.ClientMatchingViewset, basename='matching_client')

client_matching_router = routers.NestedSimpleRouter(router, 'matching', lookup='client_matching')
client_matching_router.register('history', matching.viewsets.ClientMatchingHistoryViewset,
                                basename='matching_client_history')
client_matching_router.register('notes', matching.viewsets.ClientMatchingNoteViewset,
                                basename='matching_client_notes')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(client_matching_router.urls)),
    path('users/me/', core.views.UsersMe.as_view(), name='users_me'),
    path('users/auth/', obtain_auth_token, name='users_auth'),
    path('dashboard/summary/', core.views.DashboardSummary.as_view(), name='dashboard_summary'),

    path('health/', core.views.HealthViewSet.as_view(), name='health'),
    path('health/', core.views.HealthViewSet.as_view(), name='health'),

    re_path('swagger(?P<format>.json|.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('sentry/', lambda x: 1 / 0, name='setry-test'),

    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
]


handler404 = core.views.error404
handler500 = core.views.error500

# this code is executed only once on server statup
logger.info('App started')
