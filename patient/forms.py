from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Patient

class PatientRegistrationForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=100,
        label='Full Name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your full name'
        })
    )
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email'
        })
    )
    gender = forms.ChoiceField(
        choices=[('', 'Select your gender'), ('M', 'Male'), ('F', 'Female')],
        label='Gender',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Create a password'
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm your password'
        })
    )
    
    class Meta:
        model = User
        fields = ('full_name', 'email', 'gender', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']

        # Debug: Print nilai gender
        print("Gender from form:", self.cleaned_data['gender'])

        # Memisahkan full_name menjadi first_name dan last_name
        full_name = self.cleaned_data['full_name'].split(' ')
        if len(full_name) > 1:
            user.first_name = full_name[0]
            user.last_name = ' '.join(full_name[1:])
        else:
            user.first_name = full_name[0]
            user.last_name = ''
        
        if commit:
            user.save()
            patient = Patient.objects.create(
                user=user,
                gender=self.cleaned_data['gender']
            )
            print("Patient created with gender:", patient.gender)
        return user
    

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email address'
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password'
        })
    )

    error_messages = {
        'invalid_login': 'Email atau password salah',
    }

class ProfileUpdateForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    gender = forms.ChoiceField(choices=Patient.GENDER_CHOICES)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['full_name'].initial = f"{user.first_name} {user.last_name}".strip()
        self.fields['email'].initial = user.email
        self.fields['gender'].initial = user.patient.gender

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude(pk=self.user.pk).filter(email=email).exists():
            raise forms.ValidationError('Email ini sudah digunakan oleh pengguna lain.')
        return email

    def save(self):
        full_name = self.cleaned_data['full_name'].split()
        email = self.cleaned_data['email']
        gender = self.cleaned_data['gender']

        # Update User
        self.user.email = email
        self.user.username = email  # Update username juga
        if len(full_name) > 1:
            self.user.first_name = full_name[0]
            self.user.last_name = ' '.join(full_name[1:])
        else:
            self.user.first_name = full_name[0]
            self.user.last_name = ''
        self.user.save()

        # Update Patient
        self.user.patient.gender = gender
        self.user.patient.save()