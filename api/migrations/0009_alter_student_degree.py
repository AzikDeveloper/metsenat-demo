# Generated by Django 3.2.9 on 2021-12-14 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_student_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='degree',
            field=models.CharField(choices=[('bachelor', 'Bakalavr'), ('master', 'Magistr'), ('doctorate', 'Doktorantura')], max_length=64, null=True),
        ),
    ]