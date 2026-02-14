from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model


User=get_user_model()

class RegisterForm (UserCreationForm):
    
    class Meta:
        model=User
        fields=['username','email','password1']

        labels={
            'username' : 'Username',
            'email' : 'Email',
        }

        help_texts = {
            'username': None,
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # remove password validation text
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None