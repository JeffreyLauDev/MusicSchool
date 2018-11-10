from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from profile.views import StudentIndexView as studentview


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return studentview(request)
    else:
        return render(request, 'home/index.html')
