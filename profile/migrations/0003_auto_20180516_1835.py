# Generated by Django 2.0.5 on 2018-05-16 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0002_auto_20180516_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qualifications',
            name='teacher',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='QUALRELNAME', serialize=False, to='profile.Teacher'),
        ),
    ]
