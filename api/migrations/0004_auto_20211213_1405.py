# Generated by Django 3.2.9 on 2021-12-13 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20211213_1324'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sponsorship',
            options={'verbose_name': 'Sponsorship', 'verbose_name_plural': 'Sponsorships'},
        ),
        migrations.AlterModelOptions(
            name='university',
            options={'verbose_name': 'University', 'verbose_name_plural': 'Universities'},
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='status',
            field=models.CharField(choices=[('new', 'Yangi'), ('processing', 'Moderatsiyada'), ('approved', 'Tasdiqlangan')], default='new', max_length=64),
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='sponsor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sponsorships', to='api.sponsor'),
        ),
        migrations.AlterField(
            model_name='student',
            name='degree',
            field=models.CharField(choices=[('Bachelor', 'Bakalavr'), ('Master', 'Magistr'), ('Doctorate', 'Doktorantura')], max_length=64, null=True),
        ),
    ]
