from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()
# Create your models here.

class StudentProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    roll_number=models.IntegerField(null=True,blank=True)
    education=models.CharField(max_length=100,null=True,blank=True)
    year_of_admission=models.IntegerField(null=True,blank=True)
    date_of_birth=models.DateField(null=True,blank=True)
    
    profile_pic=models.ImageField(upload_to='profile_pics/',default='profile_pics/def.png',blank=True,null=True)
    def __str__(self):
        return self.user.username
    

class Course(models.Model):
    title=models.CharField(max_length=100,default='Untitled')
    description=models.TextField(default='No description')
    price=models.IntegerField(default=0)
    image=models.ImageField(upload_to='course_images/',blank=True,null=True)

class Purchase(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True,blank=True)
    purchased_at= models.DateField(auto_now_add=True)