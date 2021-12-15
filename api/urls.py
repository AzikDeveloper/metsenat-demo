from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('sponsors', SponsorView.as_view()),
    path('sponsors/<int:pk>', SponsorDetailView.as_view()),
    path('students', StudentView.as_view()),
    path('students/<int:pk>', StudentDetailView.as_view()),
    path('sponsorships', SponsorshipView.as_view()),
    path('sponsorships/<int:pk>', SponsorshipDetailView.as_view()),
    path('universities', UniversityView.as_view()),
    path('universities/<int:pk>', UniversityDetailView.as_view()),
    path('dashboard', DashboardView.as_view())
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
