from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

#===============================================================================#
#                               Enums used in models                            #
#===============================================================================#
# enum for gender choice
GENDERCHOICE = (
    ('MA', 'Male'),
    ('FE', 'Female'),
    ('OT', 'Other'),
)

# enum for language choice
LANGUAGECHOICE = (
    ('EN', 'English'),
    ('MA', 'Mandarin'),
    ('JA', 'Japanese'),
    ('GE', 'German'),
    ('FR', 'French'),
    ('SP', 'Spanish'),
)

# enum for instrument choice
INSTRUMENTCHOICES = (
    ('PI', 'Piano'),
    ('GU', 'Guitar'),
    ('HA', 'Harmonium'),
    ('TU', 'Tuba'),
    ('TR', 'Trumpet'),
)


STATECHOICES = (
    ('QLD', 'Queensland'),
    ('NSW', 'New South Wales'),
    ('TAS', 'Tasmania'),
    ('VIC' 'Victoria'),
    ('WAT', 'Western Australia'),
    ('SAH', 'South Australia'),
    ('NTH', 'Nothern Territory'),
)

DURATIONCHOICES = (
    ('30', '30'),
    ('60', '60'),
)

#===============================================================================#
#                               Database models                                 #
#===============================================================================#

# Basic information relating to all profiles (people).
class Profile(models.Model):
    # Personal info
    gender = models.CharField(max_length=2, choices=GENDERCHOICE)
    dob = models.DateField(max_length=8)
    phone = models.CharField(max_length=10)

    # Address info
    street_number = models.IntegerField(null=True, blank=True)
    street_name = models.CharField(max_length=254, null=True, blank=True)
    suburb = models.CharField(max_length=254, null=True, blank=True)
    postcode = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=3, null=True)

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    #user = models.OneToOne(User)

    
    class Meta:
        abstract = True

# Profile subclass
class Teacher(Profile):
    def get_absolute_url(self):
        return reverse('profile:teacher_settings', kwargs={'pk': self.pk})

# Profile subclass
class Student(Profile):
    other_phone = models.CharField(max_length=10, null=True, blank=True)
    facebook = models.CharField(max_length=254, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('profile:settings', kwargs={'pk': self.pk})

    def __str__(self):
        return "{0} {1}".format(self.user.first_name, self.user.last_name)

    #Add a function that returns if the student is over 18 or not
    #Also if the student has been at the school for over 3 months (maybe)

# Profile subclass, linked to student
class Parent(Profile):
    # TODO: limit_choices_to dob < today-18yr
    child = models.ForeignKey(Student, on_delete=models.CASCADE)

class Qualifications(models.Model):
    teacher = models.OneToOneField(
        Teacher,
        on_delete = models.CASCADE,
        primary_key = True,
        related_name = 'QUALRELNAME',
    )
    # language quals
    english = models.BooleanField()
    mandarin = models.BooleanField()
    japanese = models.BooleanField()
    german = models.BooleanField()
    french = models.BooleanField()
    spanish = models.BooleanField()
    # instruments quals
    piano = models.BooleanField()
    guitar = models.BooleanField()
    tuba = models.BooleanField()
    harmonium = models.BooleanField()
    trumpet = models.BooleanField()
    
    class Meta:
        verbose_name_plural = "Qualifications"

# Table representing a student's preferences
class Preferences(models.Model):
    #All tuples related to the student preferences table
    student = models.OneToOneField(
        Student, 
        on_delete=models.CASCADE,
        primary_key=True,
    )
    teacher_pref = models.ForeignKey(
        Teacher, 
        on_delete=models.CASCADE, 
        null=True, blank=True
    )
    gender_pref = models.CharField(
        max_length=2, choices=GENDERCHOICE, null=True, blank=True
    )
    language_pref = models.CharField(
        max_length=2, choices=LANGUAGECHOICE, null=True, blank=True
    )
    instrument_pref = models.CharField(
        max_length=2, choices=INSTRUMENTCHOICES, null=True, blank=True
    )
    classtime_pref = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Preferences"
        
class Instrument(models.Model):
    INSTRUMENTCONDITION = (
        ('DI', 'discard'),
        ('RE', 'repair'),
        ('GO', 'good'),
        ('EX', 'excellent'),
        ('NE', 'new'),
    )
    type = models.CharField(max_length=2, choices=INSTRUMENTCHOICES)
    cost = models.CharField(max_length=8)
    condition = models.CharField(max_length=2, choices=INSTRUMENTCONDITION)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.type

    def get_absolute_url(self):
        return reverse('profile:index', kwargs={'pk': self.pk})

class Class(models.Model):
    class_time = models.DateTimeField()
    instrument = models.CharField(max_length=2, choices=INSTRUMENTCHOICES)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)#Should be allowed to be null
    #Change to above 2 attributes to allow for students to have multiple classes and same for teachers
    #Also change the student to null=True in the future so that it allows students to sign up for the class
    room = models.CharField(max_length=3)

    def __str__(self):
        return "{0} class by {1} at {2}".format(
            self.instrument, 
            self.teacher, 
            self.class_time
        )

class Contract(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    Teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    instrument = models.CharField(max_length=2, choices=INSTRUMENTCHOICES)
    duration = models.CharField(max_length=2, choices=DURATIONCHOICES)
    cost = models.CharField(max_length=8)

    def __str__(self):
        return "Contract between {0} and {1}".format(
            self.student.first_name,
            self.teacher.first_name,
        )

    #Create a function that auto creates weekly lessons from start date to end date

#Write the contract model and use it to fill in data pertaining to the amount of lessons a student has
