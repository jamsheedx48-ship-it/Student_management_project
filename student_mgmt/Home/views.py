from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import StudentProfile,Course,Purchase
from .forms import ProfileUpdateForm,CourseForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache
from django.contrib.auth import get_user_model
User=get_user_model()

# Create your views here.

@never_cache
@login_required(login_url='login')
def index(request):
    
    if request.user.role=='admin':
        return redirect('admin_dashboard')

    return render(request,'home.html')

@never_cache
@login_required(login_url='login')
def profile(request):
    if request.user.role=='admin':
        return redirect('admin_dashboard')
    student,_=StudentProfile.objects.get_or_create(user=request.user)

    return render(request,'profile.html',{'student':student})

@never_cache
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

@never_cache
@login_required(login_url='login')
def about(request):
    if request.user.role=='admin':
        return redirect('admin_dashboard')
    return render(request,'about.html')

@never_cache
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

@never_cache
@login_required
def buy_course(request,id):
    if request.user.role=='admin':
        return redirect('admin_dashboard')
    course = get_object_or_404(Course, id=id)

    if not Purchase.objects.filter(user=request.user,course=course).exists():
        Purchase.objects.create(user=request.user,course=course)
        messages.success(request,'Course Purchased')
    else:
        messages.error(request,'You already purchased thi course')    
    return redirect('courses')

@never_cache
@login_required
def my_courses(request):
    if request.user.role=='admin':
        return redirect('admin_dashboard')
    purchases=Purchase.objects.filter(user=request.user)
    return render(request,'mycourses.html',{'purchases':purchases})

@never_cache
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

@never_cache
@login_required(login_url='login')
def edit_student(request,id):
    if request.user.role != 'admin':
        return redirect('index')

    user = get_object_or_404(User, id=id)
    profile,_=StudentProfile.objects.get_or_create(user=user)

    if request.method=='POST':
        form=ProfileUpdateForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            profile=form.save(commit=False)

            user.email=form.cleaned_data['email']
            user.save()

            profile.save()
            messages.success(request,'Profile updted')
            return redirect('admin_dashboard')
    else:
        form=ProfileUpdateForm(
            instance=profile,
            initial={'email':user.email}
            )
    return render(request,'edit_student.html',{'form':form})

@never_cache
@login_required(login_url='login') 
def delete_student(request,id):
    if request.user.role != 'admin':
        return redirect('index')
    
    user = get_object_or_404(User, id=id)
    if request.method=='POST':
        user.delete()
        messages.success(request,'Student deleted')
        return redirect('admin_dashboard')
    
    return redirect('admin_dashboard')

    
@never_cache    
@login_required(login_url='login')
def admin_courses(request):
    if request.user.role != 'admin':
        return redirect('index')
    courses=Course.objects.all().order_by('-id')

    return render(request,'admin_courses.html',{
        'courses':courses
    })

@never_cache
@login_required(login_url='login')
def add_course(request):
    if request.user.role != 'admin':
        return redirect('index')
    if request.method=='POST':
        form=CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Course Added Successfully')
            return redirect('admin_courses')

    form=CourseForm()
    return render(request,'add_course.html',{
        'form':form
    })
    
@never_cache    
@login_required(login_url='login')
def edit_course(request,id):
    if request.user.role != 'admin':
        return redirect('index')
    
    course = get_object_or_404(Course, id=id)
    if request.method=='POST':
        form=CourseForm(request.POST , instance=course)
        if form.is_valid():
            form.save()
            messages.success(request,'Course Updated')
            return redirect('admin_courses')

    form=CourseForm(instance=course)
    return render(request,'edit_courses.html',{
        'form':form
    })

@never_cache
@login_required(login_url='login')
def delete_course(request,id):
    if request.user.role != 'admin':
        return redirect('index')
    
    if request.method=='POST':
        course = get_object_or_404(Course, id=id)
        course.delete()
        messages.success(request,'Course Deleted')
        return redirect('admin_courses')
    return redirect('admin_courses')

@never_cache
@login_required(login_url='login')
def course_detail(request,id):
    if request.user.role != 'admin':
        return redirect('index')
    
    course = get_object_or_404(Course, id=id)

    return render(request,'course_detail.html',{
        'course':course
    })