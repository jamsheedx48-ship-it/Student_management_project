from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib import messages
from .forms import RegisterForm
# Create your views here.

def register_view(request):
    if request.method=='POST':
       form=RegisterForm(request.POST)
       if form.is_valid():
           user=form.save(commit=False)
           user.is_active=False
           user.save()

           uid = urlsafe_base64_encode(force_bytes(user.pk))
           token = default_token_generator.make_token(user)

           domain = get_current_site(request).domain
           link = f"http://{domain}/auth/verify/{uid}/{token}/"

           send_mail(
                "Verify your account",
                f"Click to verify: {link}",
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
           messages.success(request,'Check your email to verify account.')
           return redirect('login')
       else:
           messages.error(request, "Please correct the errors.")
       
           
           

    else:
        form=RegisterForm()
    
        
    return render(request,'register.html',{'form':form})

def login_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request,username=username,password=password)
        if user is not None and user.is_active:
            login(request,user)
            messages.success(request,'Login success')
            return redirect('index')
        elif user is not None and not user.is_active:
            messages.info(request,'Please verify your email first.')
        else:
            messages.error(request,'Invalid username or password')
    return render(request,'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
User = get_user_model()

def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Email verified successfully. You can login.")
        return redirect('login')
    else:
        return HttpResponse("Invalid verification link.")