from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    """Extended user creation form with email and name fields."""
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl bg-brand-800/50 border border-accent-400/30 text-cream-50 theme-light:text-brand-900 theme-light:bg-cream-50 theme-light:border-brand-300 placeholder-cream-500 theme-light:placeholder-brand-400 focus:outline-none focus:border-accent-400 focus:ring-2 focus:ring-accent-400/50 transition-all',
            'placeholder': 'First name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl bg-brand-800/50 border border-accent-400/30 text-cream-50 theme-light:text-brand-900 theme-light:bg-cream-50 theme-light:border-brand-300 placeholder-cream-500 theme-light:placeholder-brand-400 focus:outline-none focus:border-accent-400 focus:ring-2 focus:ring-accent-400/50 transition-all',
            'placeholder': 'Last name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl bg-brand-800/50 border border-accent-400/30 text-cream-50 theme-light:text-brand-900 theme-light:bg-cream-50 theme-light:border-brand-300 placeholder-cream-500 theme-light:placeholder-brand-400 focus:outline-none focus:border-accent-400 focus:ring-2 focus:ring-accent-400/50 transition-all',
            'placeholder': 'Email address'
        })
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-brand-800/50 border border-accent-400/30 text-cream-50 theme-light:text-brand-900 theme-light:bg-cream-50 theme-light:border-brand-300 placeholder-cream-500 theme-light:placeholder-brand-400 focus:outline-none focus:border-accent-400 focus:ring-2 focus:ring-accent-400/50 transition-all',
                'placeholder': 'Username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl bg-brand-800/50 border border-accent-400/30 text-cream-50 theme-light:text-brand-900 theme-light:bg-cream-50 theme-light:border-brand-300 placeholder-cream-500 theme-light:placeholder-brand-400 focus:outline-none focus:border-accent-400 focus:ring-2 focus:ring-accent-400/50 transition-all',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl bg-brand-800/50 border border-accent-400/30 text-cream-50 theme-light:text-brand-900 theme-light:bg-cream-50 theme-light:border-brand-300 placeholder-cream-500 theme-light:placeholder-brand-400 focus:outline-none focus:border-accent-400 focus:ring-2 focus:ring-accent-400/50 transition-all',
            'placeholder': 'Confirm password'
        })


class CustomUserChangeForm(UserChangeForm):
    """Extended user change form for profile updates."""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-brand-800/50 border border-accent-400/30 text-cream-50 theme-light:text-brand-900 theme-light:bg-cream-50 theme-light:border-brand-300 placeholder-cream-500 theme-light:placeholder-brand-400 focus:outline-none focus:border-accent-400 focus:ring-2 focus:ring-accent-400/50 transition-all',
                'placeholder': 'First name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-brand-800/50 border border-accent-400/30 text-cream-50 theme-light:text-brand-900 theme-light:bg-cream-50 theme-light:border-brand-300 placeholder-cream-500 theme-light:placeholder-brand-400 focus:outline-none focus:border-accent-400 focus:ring-2 focus:ring-accent-400/50 transition-all',
                'placeholder': 'Last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-brand-800/50 border border-accent-400/30 text-cream-50 theme-light:text-brand-900 theme-light:bg-cream-50 theme-light:border-brand-300 placeholder-cream-500 theme-light:placeholder-brand-400 focus:outline-none focus:border-accent-400 focus:ring-2 focus:ring-accent-400/50 transition-all',
                'placeholder': 'Email address'
            }),
        }


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating user profile picture."""
    class Meta:
        model = Profile
        fields = ('profile',)
        widgets = {
            'profile': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-cream-200 theme-light:text-brand-800 file:mr-4 file:py-2.5 file:px-4 file:rounded-lg file:border-0 file:bg-accent-500 file:text-brand-900 file:font-semibold hover:file:bg-accent-600 transition-all',
                'accept': 'image/*'
            }),
        }


class LoginForm(forms.Form):
    """Custom login form with styled fields."""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl bg-brand-800/50 border border-accent-400/30 text-cream-50 theme-light:text-brand-900 theme-light:bg-cream-50 theme-light:border-brand-300 placeholder-cream-500 theme-light:placeholder-brand-400 focus:outline-none focus:border-accent-400 focus:ring-2 focus:ring-accent-400/50 transition-all',
            'placeholder': 'Email or username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl bg-brand-800/50 border border-accent-400/30 text-cream-50 theme-light:text-brand-900 theme-light:bg-cream-50 theme-light:border-brand-300 placeholder-cream-500 theme-light:placeholder-brand-400 focus:outline-none focus:border-accent-400 focus:ring-2 focus:ring-accent-400/50 transition-all',
            'placeholder': 'Password'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 rounded border-accent-400/60 text-accent-500 focus:ring-accent-400'
        })
    )
