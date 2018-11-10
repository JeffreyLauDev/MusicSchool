# Generated by Django 2.0.3 on 2018-05-29 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0011_auto_20180528_2243'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instrument',
            name='student',
        ),
        migrations.AddField(
            model_name='instrument',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='profile.Student'),
        ),
    ]