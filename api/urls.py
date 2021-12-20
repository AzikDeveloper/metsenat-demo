from django.urls import path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from .views import *

urlpatterns = [
    path('sponsors', SponsorView.as_view(), name='sponsors'),
    path('sponsors/<int:pk>', SponsorDetailView.as_view(), name='sponsor-detail'),
    path('sponsors/<int:pk>/sponsorships', SponsorshipsBySponsorView.as_view(), 'sponsorships-by-sponsor'),

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
    path('swagger', TemplateView.as_view(template_name='api/swagger-ui.html',
                                         extra_context={'schema_url': 'openapi-schema'}
                                         ), name='swagger-ui'),
    path('openapi', get_schema_view(
        title="Metsenat",
        description="API for students contract sponsorship",
        version="1.0.0"
    ), name='openapi-schema'),
]
