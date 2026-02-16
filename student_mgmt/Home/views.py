from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import StudentProfile,Course,Purchase
from .forms import ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import get_user_model
User=get_user_model()

# Create your views here.
@login_required(login_url='login')
def index(request):
    
    if request.user.role=='admin':
        return redirect('admin_dashboard')

    return render(request,'home.html')

@login_required(login_url='login')
def profile(request):
    if request.user.role=='admin':
        return redirect('admin_dashboard')
    student,_=StudentProfile.objects.get_or_create(user=request.user)

    return render(request,'profile.html',{'student':student})
@login_required(login_url='login')
def edit_profile(request):
    if request.user.role=='admin':
        return redirect('admin_dashboard')
    student,_=StudentProfile.objects.get_or_create(user=request.user)
    
    if request.method=='POST':
        form=ProfileUpdateForm(request.POST,request.FILES,instance=student)
        if form.is_valid():
            profile=form.save(commit=False)

            request.user.email=form.cleaned_data['email']
            request.user.save()

            profile.save()
            messages.success(request,'Profile updted')
            return redirect('profile')
    else:
        form=ProfileUpdateForm(
        instance=student,
        initial={'email':request.user.email}
    )
    return render(request,'editprofile.html',{'form':form})

def about(request):
    if request.user.role=='admin':
        return redirect('admin_dashboard')
    return render(request,'about.html')
@login_required
def courses(request):
    if request.user.role=='admin':
        return redirect('admin_dashboard')
    courses=Course.objects.all()
    user_purchases=Purchase.objects.filter(user=request.user)
    purchased_ids=user_purchases.values_list('course_id',flat=True)
    return render(request,'courses.html',{
        'courses':courses,
        'purchased_ids':purchased_ids
    })
@login_required
def buy_course(request,id):
    if request.user.role=='admin':
        return redirect('admin_dashboard')
    course=Course.objects.get(id=id)

    if not Purchase.objects.filter(user=request.user,course=course).exists():
        Purchase.objects.create(user=request.user,course=course)
        messages.success(request,'Course Purchased')
    else:
        messages.error(request,'You already purchased thi course')    
    return redirect('courses')
@login_required
def my_courses(request):
    if request.user.role=='admin':
        return redirect('admin_dashboard')
    purchases=Purchase.objects.filter(user=request.user)
    return render(request,'mycourses.html',{'purchases':purchases})

@login_required(login_url='login')
def admin_dashboard(request):
    if request.user.role!='admin':
        return redirect('index')
    total_students=User.objects.filter(role='student').count()
    total_courses=Course.objects.count()
    total_purchases=Purchase.objects.count()
    
    students=User.objects.filter(role='student').select_related('studentprofile')
    context={
        'total_students':total_students,
        'total_courses':total_courses,
        'total_purchases':total_purchases,
        'students':students
    }
    return render(request,'admin.html',context)

def edit_student(request,id):
    student=StudentProfile.objects.get(id=id)

    if request.method=='POST':
        form=ProfileUpdateForm(request.POST,request.FILES,instance=student)
        if form.is_valid():
            profile=form.save(commit=False)

            request.user.email=form.cleaned_data['email']
            request.user.save()

            profile.save()
            messages.success(request,'Profile updted')
            return redirect('profile')
    else:
        form=ProfileUpdateForm(
            instance=student,
            initial={'email':request.user.email}
            )
    return render(request,'edit_student.html',{'form':form})
    