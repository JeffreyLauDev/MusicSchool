from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

from .models import Student, Teacher, Instrument, Class


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
    ('VIC', 'Victoria'),
    ('WAT', 'Western Australia'),
    ('SAH', 'South Australia'),
    ('NTH', 'Nothern Territory'),
)

DURATIONCHOICES = (
    ('30', '30'),
    ('60', '60'),
)

class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return self.label(obj)

class StudentSettingsForm(ModelForm):
    gender = forms.CharField(widget=forms.Select(choices=GENDERCHOICE))
    dob = forms.DateField(widget=forms.SelectDateWidget(years=range(1970, 2018)))
    phone = forms.CharField()
    other_phone = forms.CharField(required=False)
    facebook = forms.CharField(required=False)
    postcode = forms.IntegerField()
    street_name = forms.CharField()
    street_number = forms.CharField()
    suburb = forms.CharField()
    city = forms.CharField()
    state = forms.CharField(max_length=6, widget=forms.Select(choices=STATECHOICES))

    class Meta:
        model = Student
        fields = [
            'gender',
            'dob',
            'phone',
            'other_phone',
            'facebook',
            'postcode',
            'street_name',
            'street_number',
            'suburb',
            'city',
            'state'
        ]

class TeacherSettingsForm(ModelForm):
    gender = forms.CharField(widget=forms.Select(choices=GENDERCHOICE))
    dob = forms.DateField(widget=forms.SelectDateWidget(years=range(1970, 2018)))
    phone = forms.CharField()
    postcode = forms.IntegerField()
    street_name = forms.CharField()
    street_number = forms.CharField()
    suburb = forms.CharField()
    city = forms.CharField()
    state = forms.CharField(max_length=6, widget=forms.Select(choices=STATECHOICES))

    class Meta:
        model = Student
        fields = [
            'gender',
            'dob',
            'phone',
            'postcode',
            'street_name',
            'street_number',
            'suburb',
            'city',
            'state'
        ]

class UserSettingsForm(ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
        ]


class CreateClassForm(ModelForm):
    class_time = forms.DateTimeField()
    instrument = forms.CharField(widget=forms.Select(choices=INSTRUMENTCHOICES))
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all(), widget=forms.HiddenInput, required=False)
    room = forms.CharField(max_length=3)

    class Meta:
        model = Class
        fields = [
            'class_time',
            'instrument',
            'teacher',
            'room',
        ]

class EditClassForm(ModelForm):
    class_time = forms.DateTimeField()
    instrument = forms.CharField(widget=forms.Select(choices=INSTRUMENTCHOICES))
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all(), widget=forms.HiddenInput, required=False)
    student = forms.ModelChoiceField(queryset=Student.objects.all(), required=False)
    room = forms.CharField(max_length=3)

    class Meta:
        model = Class
        fields = [
            'class_time',
            'instrument',
            'teacher',
            'student',
            'room',
        ]