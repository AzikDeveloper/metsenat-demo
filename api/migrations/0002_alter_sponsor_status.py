# Generated by Django 3.2.9 on 2021-12-13 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsor',
            name='status',
            field=models.CharField(default='new', max_length=64),
        ),
    ]
