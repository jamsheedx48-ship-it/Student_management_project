from django import forms
from .models import StudentProfile,Course
class ProfileUpdateForm(forms.ModelForm):
    email=forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class':'form-control'})
        
        )
    class Meta:
        model=StudentProfile
        fields= ['roll_number','education','year_of_admission','date_of_birth','profile_pic']

        widgets = {
            'roll_number':forms.NumberInput(attrs={'class': 'form-control'}),
            'education': forms.TextInput(attrs={'class': 'form-control'}),
            'year_of_admission': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'profile_pic':forms.FileInput(attrs={'class':'form-control'})
        }
        

class CourseForm(forms.ModelForm):
    class Meta:
        model=Course
        fields='__all__'