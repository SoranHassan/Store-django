from django import forms
from .models import User, OtpCode
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField



class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError("Passords don't match")
        return cd['password2']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name', 'password', 'last_login')

class UserRegistrationForm(forms.Form):
    email = forms.EmailField(max_length=255)
    full_name = forms.CharField(max_length=255, label="Full Name")
    phone_number = forms.CharField(max_length=11)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This Email already exists.')
        return email
    
    def clean_phone(self):
        phone_number = self.cleaned_data['phone_number']
        user = User.objects.filter(phone_number=phone_number).exists()
        if user:
            raise ValidationError('This Phone number already exists.')
        OtpCode.objects.filter(phone_number=phone_number).delete()
        return phone_number

class UserLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

class VerifyCodeForm(forms.Form):
    verify_code = forms.IntegerField()