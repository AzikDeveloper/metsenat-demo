from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from . import serializers
from .permissions import IsAdminOrCreateOnly
from .models import *
from django.db.models.functions import Coalesce
from django.db import models


class SponsorsView(generics.ListCreateAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = serializers.SponsorSerializer
    # permission_classes = [IsAdminOrCreateOnly]
    filterset_fields = ['money', 'status']


class SponsorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = serializers.SponsorSerializer
    # permission_classes = [IsAdminUser]


class StudentsView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer
    # permission_classes = [IsAdminUser]
    filterset_fields = ['degree', 'university']


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer
    # permission_classes = [IsAdminUser]


class SponsorshipView(generics.ListCreateAPIView):
    queryset = Sponsorship.objects.all()
    serializer_class = serializers.SponsorshipSerializer
    # permission_classes = [IsAdminOrCreateOnly]


class SponsorshipDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sponsorship.objects.all()
    serializer_class = serializers.SponsorshipSerializer
    # permission_classes = [IsAdminOrCreateOnly]


class DashboardView(APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request):
        total_sponsored_money = Sponsorship.objects.aggregate(models.Sum('money'))['money__sum']
        total_contract_money = Student.objects.aggregate(models.Sum('contract'))['contract__sum']
        total_needed_money = total_contract_money - total_sponsored_money

        sponsors = Sponsor.objects.extra({'date_created': "date(date_created)"}).values('date_created').annotate(
            count=models.Count('id')).values_list('date_created', 'count')
        students = Student.objects.extra({'date_created': "date(date_created)"}).values('date_created').annotate(
            count=models.Count('id')).values_list('date_created', 'count')
        print(sponsors.query)
        return Response(data={
            'money_stats': {
                'total_sponsored_money': total_sponsored_money,
                'total_contract_money': total_contract_money,
                'total_needed_money': total_needed_money
            },
            'graph':
                {
                    'sponsors': sponsors,
                    'students': students
                }

        })
