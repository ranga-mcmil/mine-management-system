from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Profile
from django.forms import ClearableFileInput

# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)

CHOICES =(
    ("Miner", "Miner"),
    ("Admin", "Admin"),
)

class CustomLoginForm(AuthenticationForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['username'].widget.attrs.update(
      {'class': 'form-control form-control-lg', }
    )
    self.fields['password'].widget.attrs.update(
      {'class': 'form-control form-control-lg', }
    )



class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'andrew123',
            'name': 'usernameeee'
        }
    ))

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Andrew',
            'name': 'first_name'
        }
    ))

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Smith',
            'name': 'last_name'
        }
    ))

    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'andrew@email.com',
            'name': 'email'
        }
    ))

    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'name': 'password'
        }
    ))

    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'name': 'password'
        }
    ))
    password2 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Cornfirm Password',
            'name': 'password'
        }
    ))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords dont match')



class UserTypeForm(forms.Form):
    user_type = forms.ChoiceField(choices=CHOICES, label='Select the category', widget=forms.Select(
        attrs={
            'class': 'form-control',
            'placeholder': 'Monthly Payment',
            'label': 'sdsd'
        }
    ))

    def get_info(self):
        # Cleaned data
        cl_data = super().clean()
        user_type = cl_data.get('user_type')
        return user_type


class ProfileForm(forms.ModelForm):
    document1 = forms.FileInput(
        attrs={
            'class': 'form-control file-upload-info',
        }
    )

    document2 = forms.FileInput(
        attrs={
            'class': 'form-control file-upload-info',
        }
    )

    document3 = forms.FileInput(
        attrs={
            'class': 'form-control file-upload-info',
        }
    )

    class Meta:
        model = Profile
        fields = ('document1', 'document2', 'document3')