"""music_online_gr25 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from . import views

app_name = 'profile'

#url patterns for the profile app, both teachers and students have the same urls, however
#information is parsed in dependant on what user type is logged in
urlpatterns = [
    #Student url patterns
    #path('student/', views.RedirectTeacher, name='redirect_teacher'),
    #127.0.0.1:8000/profile/student/id=1
    path('', views.LoggedInRedirect),
    path('student', views.StudentIndexView, name='index'),
    path('student/settings', views.UpdateStudentSettings, name='settings'),
    path('student/search', views.SearchView, name='search'),
    path('student/schedule', views.StudentScheduleView, name='schedule'),

    path('hire', views.HireInstrument, name='hire-ins'),

    #Teacher url patterns
    #path('teacher/', views.RedirectTeacher, name='redirect_teacher'),
    path('teacher', views.TeacherIndexView, name='teacher_index'),
    path('teacher/settings', views.UpdateTeacherSettings, name='teacher_settings'),
    path('teacher/schedule', views.TeacherScheduleView, name='teacher_schedule'),
    path('teacher/cancel/<int:pk>', views.CancelClass.as_view(), name='cancel_class'),

    #A Javascript file that needs to be edited with django template tags
    path('custom.js<int:pk>', views.StudentScheduleTemplate.as_view(), name='student_custom'),
    path('custom.js<int:pk>', views.TeacherScheduleTemplate.as_view(), name='teacher_custom'),
]
