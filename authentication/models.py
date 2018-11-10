from django.db import models



class Student(models.Model):
    other_phone = models.CharField(max_length=10, null=True, blank=True)
    facebook = models.CharField(max_length=254, null=True, blank=True)
