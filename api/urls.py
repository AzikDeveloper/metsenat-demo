from django.urls import path, include
from .views import *
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
import debug_toolbar

# SWAGGER CONFIG
schema_view = get_schema_view(
    openapi.Info(
        title="Metsenat API",
        default_version="v1",
        description="Metsenat API",
        terms_of_service="",
        contact=openapi.Contact(email="admin@metsenat-demo.uz"),
        license=openapi.License(name="License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('sponsors', SponsorView.as_view(), name='sponsors'),
    path('sponsors/<int:pk>', SponsorDetailView.as_view(), name='sponsor-detail'),
    path('sponsors/<int:pk>/sponsorships', SponsorshipsBySponsorView.as_view(), name='sponsorships-by-sponsor'),

    path('students', StudentView.as_view(), name='students'),
    path('students/<int:pk>', StudentDetailView.as_view(), name='student-detail'),
    path('students/<int:pk>/sponsorships', SponsorshipsByStudentView.as_view(), name='sponsorships-by-students'),

    path('sponsorships', SponsorshipView.as_view(), name='sponsorships'),
    path('sponsorships/<int:pk>', SponsorshipDetailView.as_view(), name='sponsorship-detail'),

    path('universities', UniversityView.as_view(), name='universities'),
    path('universities/<int:pk>', UniversityDetailView.as_view(), name='university-detail'),

    path('dashboard', DashboardView.as_view(), name='dashboard')
]

urlpatterns += [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("__debug__/", include(debug_toolbar.urls)),
]
