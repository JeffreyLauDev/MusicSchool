# Generated by Django 2.0.5 on 2018-05-25 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0008_contract'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='cost',
            field=models.CharField(max_length=8),
        ),
    ]
