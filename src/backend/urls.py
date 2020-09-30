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
from sentry_sdk.integrations.django import DjangoIntegration
import sentry_sdk
from django.conf import settings
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
import iep.viewsets
import program.viewsets
import note.viewsets
from core.logging import logger

schema_view = get_schema_view(
    openapi.Info(
        title="GEORGIA API",
        default_version="v1",
        #   description="Test description",
        #   terms_of_service="https://www.google.com/policies/terms/",
        #   contact=openapi.Contact(email="contact@snippets.local"),
        #   license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register("clients", client.viewsets.ClientViewset, basename="client")
router.register("notes", note.viewsets.NoteViewset, basename="note")
router.register("surveys", survey.viewsets.SurveyViewset, basename="survey")
router.register("questions", survey.viewsets.QuestionViewset, basename="question")
router.register("responses", survey.viewsets.ResponseViewset, basename="response")

router.register(
    "eligibility/clients",
    eligibility.viewsets.ClientEligibilityViewset,
    basename="eligibility_clients",
)
router.register(
    "eligibility/queue",
    eligibility.viewsets.EligibilityQueueViewset,
    basename="eligibility_queue",
)
router.register("iep", iep.viewsets.ClientIEPViewset, basename="iep")
router.register(
    "programs/enrollments", program.viewsets.EnrollmentViewset, basename="enrollment"
)
# router.register('programs/eligibility', program.viewsets.ProgramEligibilityViewset,
#                 basename='eligibility')
router.register(
    "programs/services/types",
    program.viewsets.EnrollmentServiceTypeViewset,
    basename="enrollment_service_type",
)
router.register(
    "programs/services",
    program.viewsets.EnrollmentServiceViewset,
    basename="enrollment_service",
)
router.register("programs", program.viewsets.ProgramViewset, basename="program")


urlpatterns = [
    path("", include(router.urls)),
    path("users/me/", core.views.UsersMe.as_view(), name="users_me"),
    path("users/auth/", obtain_auth_token, name="users_auth"),
    path(
        "dashboard/summary/",
        core.views.DashboardSummary.as_view(),
        name="dashboard_summary",
    ),
    path("health/", core.views.HealthViewSet.as_view(), name="health"),
    re_path(
        "swagger(?P<format>.json|.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("sentry/", lambda x: 1 / 0, name="setry-test"),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
]


handler404 = core.views.error404
handler500 = core.views.error500

# this code is executed only once on server statup
logger.info("App started")


if (
    True  # settings.DEBUG is False
    and getattr(settings, "SENTRY_DSN", None) is not None
    and getattr(settings, "SENTRY_ENVIRONMENT", None) is not None
):
    print("Setting up sentry")
    sentry_sdk.init(
        dsn=str(settings.SENTRY_DSN),
        integrations=[DjangoIntegration()],
        environment=settings.SENTRY_ENVIRONMENT,
        traces_sample_rate=1.0,
        send_default_pii=True,
    )
