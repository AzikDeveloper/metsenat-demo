from rest_framework import serializers
from .models import Sponsor, Student, University, Sponsorship
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce
from .validators import (
    validate_positive,
    validate_sponsorship_money_on_update,
    validate_sponsorship_money_on_create
)


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'


class SponsorSerializer(serializers.ModelSerializer):
    spent_money = serializers.SerializerMethodField()

    class Meta:
        model = Sponsor
        fields = '__all__'
        extra_kwargs = {
            'full_name': {'allow_null': False, 'required': True},
            'phone_number': {'allow_null': False, 'required': True},
            'money': {'allow_null': False, 'required': True, 'validators': [validate_positive]},
            'person_type': {'allow_null': False, 'required': True}
        }

    def create(self, validated_data):
        validated_data['status'] = 'new'
        sponsor = Sponsor.objects.create(**validated_data)
        return sponsor

    @staticmethod
    def get_spent_money(sponsor):
        spent_money = sponsor.sponsorships.aggregate(money_sum=Coalesce(Sum('money'), 0))['money_sum']
        return spent_money

    def validate_company_name(self, value):
        if self.initial_data.get('person_type') == 'juridic':
            return value
        else:
            return None


class StudentSerializer(serializers.ModelSerializer):
    university = UniversitySerializer(read_only=True)
    university_id = serializers.IntegerField(allow_null=False, required=True, write_only=True)
    gained_money = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'full_name', 'phone_number', 'contract', 'gained_money', 'degree', 'university',
                  'university_id']

        extra_kwargs = {
            'full_name': {'allow_null': False, 'required': True},
            'phone_number': {'allow_null': False, 'required': True},
            'contract': {'allow_null': False, 'required': True, 'validators': [validate_positive]},
            'degree': {'allow_null': False, 'required': True},
        }

    @staticmethod
    def get_gained_money(student):
        gained_money = student.sponsorships.aggregate(money_sum=Coalesce(Sum('money'), 0))['money_sum']
        return gained_money


class SponsorshipSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    student_id = serializers.IntegerField(allow_null=False, required=True, write_only=True)
    sponsor = SponsorSerializer(read_only=True)
    sponsor_id = serializers.IntegerField(allow_null=False, required=True, write_only=True)

    class Meta:
        model = Sponsorship
        fields = ['id', 'student', 'student_id', 'sponsor', 'sponsor_id', 'money', 'date_created']
        extra_kwargs = {'money': {'allow_null': False, 'required': True, 'validators': [validate_positive]}}

    def update(self, instance, validated_data):
        instance = validate_sponsorship_money_on_update(instance, validated_data)
        return instance

    def create(self, validated_data):
        instance = validate_sponsorship_money_on_create(validated_data)
        return instance


class SponsorshipsByStudentSerializer(serializers.ModelSerializer):
    sponsor = serializers.SerializerMethodField()

    class Meta:
        model = Sponsorship
        fields = ['id', 'sponsor', 'money']

    @staticmethod
    def get_sponsor(sponsorship):
        data = {
            'id': sponsorship.sponsor.id,
            'full_name': sponsorship.sponsor.full_name
        }
        return data


class SponsorshipsBySponsorSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()

    class Meta:
        model = Sponsorship
        fields = ['id', 'student', 'money']

    @staticmethod
    def get_student(sponsorship):
        data = {
            'id': sponsorship.student.id,
            'full_name': sponsorship.student.full_name
        }
        return data


class DashboardMoneySerializer:
    def __init__(self):
        self.total_sponsored_money = Sponsorship.objects.aggregate(Sum('money'))['money__sum']
        self.total_contract_money = Student.objects.aggregate(Sum('contract'))['contract__sum']
        self.total_needed_money = self.total_contract_money - self.total_sponsored_money

    @property
    def data(self):
        return self.__dict__


class DashboardGraphSerializer:
    def __init__(self):
        self.sponsors_stats = Sponsor.objects.extra({'date_created': "date(date_created)"}).values(
            'date_created').annotate(
            count=Count('id')).values_list('date_created', 'count')
        self.students_stats = Student.objects.extra({'date_created': "date(date_created)"}).values(
            'date_created').annotate(
            count=Count('id')).values_list('date_created', 'count')

    @property
    def data(self):
        return self.__dict__
