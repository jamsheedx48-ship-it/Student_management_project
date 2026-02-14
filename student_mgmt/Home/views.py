from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
@login_required(login_url='login')
def index(request):
    return render(request,'home.html')
def profile(request):
    return render(request,'profile.html')
def about(request):
    return render(request,'about.html')
def courses(request):
    return render(request,'courses.html')
