from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('profile/',views.profile,name='profile'),
    path('about/',views.about,name='about'),
    path('courses/',views.courses,name='courses'),
    path('editprofile/',views.edit_profile,name='edit_profile'),
    path('buy/<int:id>',views.buy_course,name='buy_course'),
    path('mycourses/',views.my_courses,name='my_courses'),
    path('admindashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('edit_student/<int:id>',views.edit_student,name='edit_student'),
    path('delete_student/<int:id>',views.delete_student,name='delete_student'),
    path('admindashboard/courses',views.admin_courses,name='admin_courses'),
    path('admindashboard/courses/add_courses',views.add_course,name='add_courses'),
    path('admindashboard/courses/edit_courses/<int:id>',views.edit_course,name='edit_courses'),
    path('admindashboard/courses/delete_courses/<int:id>',views.delete_course,name='delete_courses'),
    path('admindashboard/courses/details/<int:id>',views.course_detail,name='course_detail')

]
