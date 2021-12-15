from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from . import serializers
from .permissions import IsAdminOrCreateOnly
from .models import *


class SponsorView(generics.ListCreateAPIView):
    # permission_classes = [IsAdminOrCreateOnly]
    queryset = Sponsor.objects.all()
    serializer_class = serializers.SponsorSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_filters = ['full_name', 'company_name']
    filterset_fields = ['money', 'status']


class SponsorDetailView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAdminUser]
    queryset = Sponsor.objects.all()
    serializer_class = serializers.SponsorSerializer


class StudentView(generics.ListCreateAPIView):
    # permission_classes = [IsAdminUser]
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['full_name']
    filterset_fields = ['degree', 'university']


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAdminUser]
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer


class SponsorshipView(generics.ListCreateAPIView):
    # permission_classes = [IsAdminOrCreateOnly]
    queryset = Sponsorship.objects.all()
    serializer_class = serializers.SponsorshipSerializer
    filter_backends = [SearchFilter]
    search_fields = ['sponsor__full_name', 'sponsor__company_name', 'student__full_name']


class SponsorshipDetailView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAdminOrCreateOnly]
    queryset = Sponsorship.objects.all()
    serializer_class = serializers.SponsorshipSerializer


class UniversityView(generics.ListCreateAPIView):
    queryset = University.objects.all()
    serializer_class = serializers.UniversitySerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


class UniversityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = University.objects.all()
    serializer_class = serializers.UniversitySerializer


class DashboardView(APIView):
    # permission_classes = [IsAdminUser]

    @staticmethod
    def get(request, *args, **kwargs):
        dashboard_money_serializer = serializers.DashboardMoneySerializer()
        dashboard_graph_serializer = serializers.DashboardGraphSerializer()
        return Response(data={
            'money_stats': dashboard_money_serializer.__dict__,
            'graph_stats': dashboard_graph_serializer.__dict__
        })
