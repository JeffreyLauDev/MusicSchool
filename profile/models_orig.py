from django.db import models

#enum for gender choice
GENDERCHOICE = (
        ('0', 'Male'),
        ('1', 'Female'),
        ('2', 'Other'),
    )

#enum for gender choice
LANGUAGECHOICE = (
        ('0', 'English'),
        ('1', 'Chinese'),
        ('2', 'Japanese'),
        ('3', 'German'),
        ('4', 'French'),
        ('5', 'Spanish'),
    )

INSTRUMENTCHOICES = (
        ('0', 'Piano'),
        ('1', 'Guitar'),
        ('2', 'Tuba'),
        ('3', 'Harmonium'),
        ('4', 'Trumpet'),
    )


# For information on al aspects of the database please refer to the ERD
#(and hopefully future relational models and normalization documents)
#The student table
class Student(models.Model):
    #Basic information relating to the student table
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDERCHOICE)
    dob = models.DateField(max_length=8)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=10)
    other_phone = models.CharField(max_length=10, null=True)
    facebook = models.CharField(max_length=254, null=True)

    # Address Model Information
    street_number = models.CharField(max_length=5)
    street_name = models.CharField(max_length=254)
    suburb = models.CharField(max_length=254)
    city = models.CharField(max_length=254)
    postcode = models.CharField(max_length=4)

    def __str__(self):
        return self.first_name

#The parent table
class Parent(models.Model):
    #Student Foreign key to link with parent data many-to-many relationship
    child = models.ForeignKey(Student, on_delete=models.CASCADE)

    #Basic information relating to the parent table
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)

#    def __str__(self):
#        return self.parent_id

#The teachers table (which may also be used for other staff members)
class Teacher(models.Model):
    #Basic information for the teacher table
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDERCHOICE)
    dob = models.DateField(max_length=8)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=10)
    other_phone = models.CharField(max_length=10, null=True)
    facebook = models.CharField(max_length=254, null=True)

    # Address Model Information
    street_number = models.CharField(max_length=5)
    street_name = models.CharField(max_length=254)
    suburb = models.CharField(max_length=254)
    city = models.CharField(max_length=254)
    postcode = models.CharField(max_length=4)

    def __str__(self):
        return self.first_name

#The teacher qualifications table
class Qualifications(models.Model):
    # All Tuples relating to the teacher qualifications
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    language_skills = models.CharField(max_length=1, choices=LANGUAGECHOICE)
    instrument_qualifications = models.CharField(max_length=254)

    def __str__(self):
        return self.qualifications_id

#The table for student that will indicate student preferences
class Preferences(models.Model):
    #All tuples related to the student preferences table
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher_preferences = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    gender_preferences = models.CharField(max_length=1, choices=GENDERCHOICE, null=True)
    language_preferences = models.CharField(max_length=1, choices=LANGUAGECHOICE, null=True)
    date_time_preferences = models.DateTimeField()

    def __str__(self):
        return self.preferences_id

class Instrument(models.Model):

    INSTRUMENTCONDITION = (
        ('0', 'discard'),
        ('1', 'repair'),
        ('2', 'good'),
        ('3', 'excellent'),
        ('4', 'new'),
    )
    type = models.CharField(max_length=1, choices=INSTRUMENTCHOICES)
    cost = models.CharField(max_length=8)
    condition = models.CharField(max_length=1, choices=INSTRUMENTCONDITION)
    student = models.ManyToManyField(Student)

    def __str__(self):
        return self.type

class Classes(models.Model):

    time = models.TimeField()
    date = models.DateField()
    instrumentType = models.CharField(max_length=1, choices=INSTRUMENTCHOICES)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ManyToManyField(Student)

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

"""
This is a test for using inheritance in database models

class User(models.Model):
    #Enum for gender
    GENDERCHOICE = (
        ('0', 'Male'),
        ('1', 'Female'),
        ('2', 'Other'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDERCHOICE)
    dob = models.DateField(max_length=8)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=10)
    facebook = models.CharField(max_length=254, null=True)

    #Address Model Information
    street_number = models.CharField(max_length=5)
    street_name = models.CharField(max_length=254)
    suburb = models.CharField(max_length=254)
    city = models.CharField(max_length=254)
    postcode = models.CharField(max_length=4)

    class Meta:
        abstract = True
"""
