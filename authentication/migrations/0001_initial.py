# Generated by Django 2.0.5 on 2018-05-28 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('other_phone', models.CharField(blank=True, max_length=10, null=True)),
                ('facebook', models.CharField(blank=True, max_length=254, null=True)),
            ],
        ),
    ]