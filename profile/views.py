from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.utils.cache import add_never_cache_headers
from django.contrib.auth.models import User

from django.template import RequestContext

from .models import Student, Teacher, Qualifications, Preferences, Parent, Class, Instrument

from .forms import StudentSettingsForm, TeacherSettingsForm, UserSettingsForm, CreateClassForm, EditClassForm

from datetime import date


# The home page view of the user profile, only accomdates the student page currently

# Student Views

# The view for the index page of the users
# will eventually determine which user is currently using the system and
# render the correct template

def LoggedInRedirect(request):
    if not request.user.is_authenticated:
        return redirect('/home/')

    if not request.user.is_staff:
        return redirect('/profile/student')
    elif request.user.is_superuser:
        return redirect('/admin')
    elif request.user.is_staff:
        return redirect('/profile/teacher')

# ================================================================================
#                               Student Views
# ================================================================================

# Redirects the student user to their user page
def StudentIndexView(request):
    if not request.user.is_staff and request.user.is_authenticated:
        lessons = Class.objects.filter(student=request.user.student)
        instruments = Instrument.objects.all()

        #Return all instruments unless an instruments is already hired

        if request.method == 'POST':
            ins = Instrument.objects.get(pk=request.POST['ins_id'])
            ins.student.add(request.user.student)
            ins.save()

        return render(request, 'profile/student-pannel-index.html', {'lessons': lessons, 'instruments': instruments})
    return redirect('authentication:login')


def HireInstrument(request):
    if request.user.is_staff or not request.user.is_authenticated:
        redirect('/authentication/login')

    if request.method == 'POST':
        ins = Instrument.objects.get(pk=request.POST['ins_id'])

        if request.POST['hire'] == "yes":
            ins.student = request.user.student
            ins.save()
        elif request.POST['hire'] == "no":
            ins.student = None
            ins.save()

    lessons = Class.objects.filter(student=request.user.student)
    instruments = Instrument.objects.all()

    return render(request, 'profile/student-pannel-index.html', {'lessons': lessons, 'instruments': instruments})
    

# Updates the students settings using values they enter in
def UpdateStudentSettings(request):
    if request.user.is_staff != True and request.user.is_authenticated:
        instanceStudent = Student.objects.get(id=request.user.student.id)
        instanceUser = User.objects.get(id=request.user.id)
        userSetting = UserSettingsForm(request.POST, instance=instanceStudent)
        studentSetting = StudentSettingsForm(request.POST, instance=instanceUser)

        if request.method == 'POST':
            userForm = UserSettingsForm(request.POST, prefix="userSetting", instance=instanceUser)
            studentForm = StudentSettingsForm(request.POST, prefix="studentSetting", instance=instanceStudent)

            if userForm.is_valid() and studentForm.is_valid():
                userForm.save(commit=False)
                studentForm.save(commit=False)

                userForm.user = request.user
                studentForm.student = request.user.student

                userForm.save()
                studentForm.save()

                return redirect('profile:settings')

        else:
            userSetting = UserSettingsForm(prefix="userSetting")
            studentSetting = StudentSettingsForm(prefix="studentSetting")

        return render(request, 'profile/student-pannel-setting.html',
                      {'userSetting': userSetting, 'studentSetting': studentSetting})
    return redirect('authentication:login')


# View that allows a student to search through available lessons to sign up for
# Change to a function based view they are much much better
def SearchView(request):
    if request.user.is_staff != True and request.user.is_authenticated:

        if request.method == 'POST':
            cla = Class.objects.get(pk=request.POST['class_id'])
            cla.student = request.user.student
            cla.save()

        classes = Class.objects.filter(student__isnull=True)
        return render(request, 'profile/pannel-course.html', {'classes': classes})
    return redirect('authentication:login')


# View that shows the student a graphical version of their timetable

def StudentScheduleView(request):
    if request.user.is_staff != True and request.user.is_authenticated:
        lessons = Class.objects.filter(student=request.user.student)
        return render(request, 'profile/pannel-schedule.html', {'lessons': lessons})
    return redirect('authentication:login')


# ================================================================================
#                               Teacher Views
# ================================================================================

# View that renders the teachers home page along with all necassary information about their classes
def TeacherIndexView(request):
    if request.user.is_staff and request.user.is_authenticated:

        classCreation = CreateClassForm(request.POST)
        classEdit = EditClassForm(request.POST)
        lessons = Class.objects.filter(teacher=request.user.teacher)

        if request.method == 'POST':

            if 'create' in request.POST:
                classFormCreate = CreateClassForm(request.POST, prefix="classCreation")

                class_timeInput = classFormCreate["class_time"].value()
                instrumentInput = classFormCreate["instrument"].value()
                teacherInput = request.user.teacher
                roomInput = classFormCreate["room"].value()

                if classFormCreate.is_valid():
                    Class.objects.create(class_time=class_timeInput, instrument=instrumentInput, teacher=teacherInput,
                                         room=roomInput)
                    return redirect('profile:teacher_index')

            elif 'edit' in request.POST:
                classFormEdit = EditClassForm(request.POST, prefix="classEdit")

                class_timeInput = classFormEdit["class_time"].value()
                instrumentInput = classFormEdit["instrument"].value()
                teacherInput = request.user.teacher
                roomInput = classFormEdit["room"].value()

                if classFormEdit["student"] == None:
                    studentInput = Student.objects.get(pk=classFormEdit["student"].value() or None)
                else:
                    studentInput = None

                print (class_timeInput, instrumentInput, teacherInput, studentInput, roomInput)

                if classFormEdit.is_valid():
                    c = Class.objects.get(pk=request.POST['class_id'])
                    c.class_time = class_timeInput
                    c.instrument = instrumentInput
                    c.teacher = teacherInput
                    c.student = studentInput
                    c.room = roomInput
                    c.save()

                    return redirect('profile:teacher_index')

        else:
            classCreation = CreateClassForm(prefix="classCreation")
            classEdit = EditClassForm(prefix="classEdit")

        return render(request, 'profile/teacher-pannel-index.html',
                      {'classCreation': classCreation, 'classEdit': classEdit,
                       'lessons': lessons})
    return redirect('authentication:login')


# Updates the teachers profile with information given by them
def UpdateTeacherSettings(request):
    if request.user.is_staff == True and request.user.is_authenticated:
        instanceTeacher = Teacher.objects.get(id=request.user.teacher.id)
        instanceUser = User.objects.get(id=request.user.id)
        userSetting = UserSettingsForm(request.POST, instance=instanceTeacher)
        teacherSetting = TeacherSettingsForm(request.POST, instance=instanceUser)

        if request.method == 'POST':
            userForm = UserSettingsForm(request.POST, prefix="userSetting", instance=instanceUser)
            teacherForm = TeacherSettingsForm(request.POST, prefix="teacherSetting", instance=instanceTeacher)

            if userForm.is_valid() and teacherForm.is_valid():
                userForm.save(commit=False)
                teacherForm.save(commit=False)

                userForm.user = request.user
                teacherForm.teacher = request.user.teacher

                userForm.save()
                teacherForm.save()

                return redirect('profile:teacher_settings')

        else:
            userSetting = UserSettingsForm(prefix="userSetting")
            teacherSetting = TeacherSettingsForm(prefix="teacherSetting")

        return render(request, 'profile/teacher-pannel-setting.html',
                      {'userSetting': userSetting, 'teacherSetting': teacherSetting})
    return redirect('authentication:login')


# Shows that teacher a graphical version of their timetable
def TeacherScheduleView(request):
    if request.user.is_staff and request.user.is_authenticated:
        lessons = Class.objects.filter(teacher=request.user.teacher)
        return render(request, 'profile/pannel-schedule-staff.html', {'lessons': lessons})
    return redirect('authentication:login')


# To be completed
class CancelClass(DeleteView):
    model = Class
    success_url = reverse_lazy('profile:teacher_index')


# To be completed
def CreateClass(request):
    if request.user.is_staff == True and request.user.is_authenticated:
        classCreation = CreateClassForm(request.POST)

        if request.method == 'POST':
            classForm = CreateClassForm(request.POST, prefix="classCreation")

            if classForm.is_valid():
                classForm.save()
                return redirect('profile:teacher_index')

        else:
            classCreation = CreateClassForm(prefix="classCreation")

        return render(request, 'profile/teacher-pannel-index.html', {'classCreation': classCreation})
    return redirect('authentication:login')


# ================================================================================
#                               Javascript Views
# ================================================================================

# Retrieves a javascript file for the student timetable
class StudentScheduleTemplate(generic.TemplateView):
    template_name = 'profile/custom.js'

    # Sends data on lessons relevant to the student so that the timetable can be populated
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lessons'] = Class.objects.filter(student=Student.objects.get(pk=self.kwargs['pk']))
        return context

    def process_response(self, request, response):
        add_never_cache_headers(response)
        return response


# Retrieves a javascript file for the teacher timetable
class TeacherScheduleTemplate(generic.TemplateView):
    template_name = 'profile/custom.js'

    # Sends data on lessons relevant to the teacher so that the timetable can be populated
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lessons'] = Class.objects.filter(teacher=Teacher.objects.get(pk=self.kwargs['pk']))
        return context

    def process_response(self, request, response):
        add_never_cache_headers(response)
        return response


"""
Notes:

class StudentIndexView(generic.DetailView):
    model = Student
    template_name = 'profile/student-pannel-index.html'

    #Sends data on the lessons that the student may have
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lessons'] = Class.objects.filter(student_id=self.kwargs['pk'])
        context['instruments'] = Instrument.objects.all()
        return context
        INSERT INTO profile_teacher VALUES(1, 'FE', '1972-03-07', '0473849287', 4055, 'McGregor Way', 20, 'somewhere', 'Ferny Grove', 'Brisbane', 'QLD', '3')

class UpdateStudentSettings(UpdateView):
    model = Student
    fields = ['first_name', 'last_name', 'gender', 'dob', 'email', 'phone',
              'street_number', 'street_name', 'suburb', 'postcode', 'city', 'state',
              'other_phone', 'facebook']
    template_name_suffix = '-pannel-setting'

    #Sends data on the preferences that the user has
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pref'] = Preferences.objects.filter(student_id=self.kwargs['pk'])
        return context

        class StudentScheduleView(generic.DetailView):
    model = Student
    template_name = 'profile/pannel-schedule.html'

    #Dynamically reloads javascript so that it may be used for the graphical schedule
    def process_response(self, request, response):
        add_never_cache_headers(response)
        return response

    #Sends data on lessons relevant to the student so that the timetable can be populated
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lessons'] = Class.objects.filter(student_id=self.kwargs['pk'])
        return context
"""
