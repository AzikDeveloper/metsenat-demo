from django.db import models


class Sponsor(models.Model):
    STATUS_CHOICES = (
        ('new', 'Yangi'),
        ('processing', 'Moderatsiyada'),
        ('approved', 'Tasdiqlangan'),
        ('canceled', 'Bekor qilingan')
    )
    PERSON_CHOICES = (
        ('physical', 'Jismoniy shaxs'),
        ('juridic', 'Yuridik shaxs')
    )
    full_name = models.CharField(max_length=128, null=True)
    phone_number = models.CharField(max_length=13, null=True)
    money = models.BigIntegerField(null=True)
    person_type = models.CharField(max_length=16, choices=PERSON_CHOICES, null=True)
    company_name = models.CharField(max_length=256, null=True, blank=True)
    status = models.CharField(max_length=64, choices=STATUS_CHOICES, default='new')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name if self.full_name else super().__str__()


class University(models.Model):
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'University'
        verbose_name_plural = 'Universities'


class Student(models.Model):
    DEGREE_CHOICES = (
        ('bachelor', 'Bakalavr'),
        ('master', 'Magistr'),
        ('doctorate', 'Doktorantura')
    )
    full_name = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=13, null=True)
    university = models.ForeignKey(University, related_name='students', on_delete=models.SET_NULL, null=True)
    degree = models.CharField(max_length=64, choices=DEGREE_CHOICES, null=True)
    contract = models.BigIntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name if self.full_name else super().__str__()


class Sponsorship(models.Model):
    sponsor = models.ForeignKey(Sponsor, related_name='sponsorships', on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, related_name='sponsorships', on_delete=models.CASCADE, null=True)
    money = models.BigIntegerField(null=True)

    def __str__(self):
        try:
            return f'{self.sponsor.full_name} -> {self.student.full_name} : {self.money} so\'m'
        except Exception:
            return super().__str__()

    class Meta:
        verbose_name = 'Sponsorship'
        verbose_name_plural = 'Sponsorships'
