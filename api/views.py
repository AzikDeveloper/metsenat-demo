from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .permissions import IsAdminOrCreateOnly
from .filters import DateRangeFilterBackend
from . import serializers
from .models import *


class SponsorView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrCreateOnly]
    queryset = Sponsor.objects.all()
    serializer_class = serializers.SponsorSerializer
    filter_backends = [DateRangeFilterBackend, SearchFilter, DjangoFilterBackend]
    search_fields = ['full_name', 'company_name']
    filterset_fields = ['money', 'status']
    date_range_filter_field = 'date_created'


class SponsorDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Sponsor.objects.all()
    serializer_class = serializers.SponsorSerializer


class StudentView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer
    filter_backends = [DateRangeFilterBackend, SearchFilter, DjangoFilterBackend]
    search_fields = ['full_name']
    filterset_fields = ['degree', 'university']
    date_range_filter_field = 'date_created'


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer


class SponsorshipView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Sponsorship.objects.all()
    serializer_class = serializers.SponsorshipSerializer
    filter_backends = [DateRangeFilterBackend, SearchFilter, DjangoFilterBackend]
    search_fields = ['sponsor__full_name', 'sponsor__company_name', 'student__full_name']
    date_range_filter_field = 'date_created'


class SponsorshipDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Sponsorship.objects.all()
    serializer_class = serializers.SponsorshipSerializer


class SponsorshipsByStudentView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = serializers.SponsorshipsByStudentSerializer

    def get_queryset(self):
        student = get_object_or_404(Student, id=self.kwargs['pk'])
        queryset = student.sponsorships.all()
        return queryset


class SponsorshipsBySponsorView(generics.ListAPIView):
    # permission_classes = [IsAdminUser]
    serializer_class = serializers.SponsorshipsBySponsorSerializer

    def get_queryset(self):
        sponsor = get_object_or_404(Sponsor, id=self.kwargs['pk'])
        queryset = sponsor.sponsorships.all()
        return queryset


class UniversityView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = University.objects.all()
    serializer_class = serializers.UniversitySerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


class UniversityDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = University.objects.all()
    serializer_class = serializers.UniversitySerializer


class DashboardView(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def get(request, *args, **kwargs):
        dashboard_money_serializer = serializers.DashboardMoneySerializer()
        dashboard_graph_serializer = serializers.DashboardGraphSerializer()
        return Response(data={
            'money_stats': dashboard_money_serializer.data(),
            'graph_stats': dashboard_graph_serializer.data()
        })
