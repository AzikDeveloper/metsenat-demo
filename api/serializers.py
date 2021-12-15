from rest_framework import serializers
from .models import Sponsor, Student, University, Sponsorship
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce
from rest_framework.validators import ValidationError
from django.shortcuts import get_object_or_404
from .validators import validate_positive


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

    def get_spent_money(self, sponsor):
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

    def get_gained_money(self, student):
        gained_money = student.sponsorships.aggregate(money_sum=Coalesce(Sum('money'), 0))['money_sum']
        return gained_money


class SponsorshipSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    student_id = serializers.IntegerField(allow_null=False, required=True, write_only=True)
    sponsor = SponsorSerializer(read_only=True)
    sponsor_id = serializers.IntegerField(allow_null=False, required=True, write_only=True)

    class Meta:
        model = Sponsorship
        fields = ['id', 'student', 'student_id', 'sponsor', 'sponsor_id', 'money']
        extra_kwargs = {'money': {'allow_null': False, 'required': True, 'validators': [validate_positive]}}

    def update(self, instance, validated_data):
        sponsor = get_object_or_404(Sponsor, id=validated_data['sponsor_id'])
        student = instance.student
        money = validated_data['money']

        sponsor_spent_money = \
            sponsor.sponsorships.exclude(id=instance.id).aggregate(money_sum=Coalesce(Sum('money'), 0))['money_sum']
        student_gained_money = \
            student.sponsorships.exclude(id=instance.id).aggregate(money_sum=Coalesce(Sum('money'), 0))['money_sum']
        sponsor_left_money = sponsor.money - sponsor_spent_money

        if money <= sponsor_left_money:
            if student_gained_money + money <= instance.student.contract:
                instance.money = money
                instance.sponsor = sponsor
                instance.save()
                return instance
            else:
                raise ValidationError({'money': 'Homiylik puli kontrakt miqdoridan oshib ketdi'})
        else:
            raise ValidationError({'money': 'Homiyda buncha pul mavjud emas.'})

    def create(self, validated_data):
        sponsor = get_object_or_404(Sponsor, id=validated_data.get('sponsor_id'))
        student = get_object_or_404(Student, id=validated_data.get('student_id'))
        money = validated_data.get('money')

        sponsor_spent_money = sponsor.sponsorships.aggregate(money_sum=Coalesce(Sum('money'), 0))['money_sum']
        student_gained_money = student.sponsorships.aggregate(money_sum=Coalesce(Sum('money'), 0))['money_sum']
        sponsor_left_money = sponsor.money - sponsor_spent_money

        if money <= sponsor_left_money:
            if student_gained_money + money <= student.contract:
                sponsorship = Sponsorship.objects.create(**validated_data)
                return sponsorship
            else:
                raise ValidationError({'money': 'Homiylik puli kontrakt miqdoridan ochib ketdi'})
        else:
            raise ValidationError({'money': 'Homiyda buncha pul mavjud emas.'})


class DashboardMoneySerializer:
    def __init__(self):
        self.total_sponsored_money = Sponsorship.objects.aggregate(Sum('money'))['money__sum']
        self.total_contract_money = Student.objects.aggregate(Sum('contract'))['contract__sum']
        self.total_needed_money = self.total_contract_money - self.total_sponsored_money

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

    def data(self):
        return self.__dict__
