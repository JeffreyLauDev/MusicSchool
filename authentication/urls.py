from django.urls import path, include
from . import views
from .forms import userLoginForm 


app_name = 'authentication'

urlpatterns = [
   path('login/', views.login_view, name='login'),
   path('signup/', views.signup_view, name='signup'),
   path('logout/', views.logout_view, name='logout'),
]