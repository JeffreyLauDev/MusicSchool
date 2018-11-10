from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import userLoginForm, signupForm, StudentSignupForm
from profile.models import Student


# Create your views here.

def login_view(request):
    print(request.user.is_authenticated)
    print(request.user)
    
    form = userLoginForm(request.POST or None)

    if form.is_valid():
        print("LOGIN page")
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("/profile/")

#    if request.user.is_authenticated and not request.user.is_staff:
#        return redirect("profile/student")
#
#    if request.user.is_superuser:
#        return  redirect("admin:index")
#
#    if request.user.is_authenticated and request.user.is_staff == True:
#        return  redirect("profile/teacher")

    return render(request, 'authentication/login.html', {"form":form})

def logout_view(request):

    logout(request)
    return render(request, 'home/index.html')

def signup_view(request):

    form = signupForm(request.POST or None)
    form2 = StudentSignupForm(request.POST or None)

    #Add a user_id to the student form (For reference look at profile/forms.py StudentSettingsForm
    if request.user.is_authenticated:
        return redirect("profile:index")
    if form.is_valid() and form2.is_valid():

        user = form.save(commit=False)
        password = form.cleaned_data.get("password")
        user.set_password(password)

        user.save()


        new_user = authenticate(username=user.username, password=password)
        login(request, user)
        genderRadios = form2["gender"].value()
        inputDateOfBirth = form2["dob"].value()
        inputMobilePhone = form2["phone"].value()
        inputOtherPhone = form2["other_phone"].value()
        inputFacebook = form2["facebook"].value()
        inputZip = form2["postcode"].value()
        inputStreetName = form2["street_name"].value()
        inputStreetNum = form2["street_number"].value()
        inputSuburb = form2["suburb"].value()
        inputAddress2 = form2["city"].value()
        inputState = form2["state"].value()
        Student.objects.create(gender = genderRadios,dob = inputDateOfBirth,phone = inputMobilePhone,other_phone = inputOtherPhone, facebook = inputFacebook, postcode =inputZip, street_name = inputStreetName, street_number = inputStreetNum,suburb = inputSuburb,city = inputAddress2,state =inputState, user = request.user)


        return redirect("profile:index")


        
    return render(request, 'authentication/signup.html', {"form":form, 'form2':form2})

