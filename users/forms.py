"""Users app form.
"""
from django.contrib.auth.forms import (UserCreationForm, AuthenticationForm,
                                       SetPasswordForm, PasswordResetForm)
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile, UserToken
from .choices import COUNTRIES


# DOCS -
# https://docs.djangoproject.com/en/1.8/_modules/django/contrib/auth/forms/
class UserForm(UserCreationForm):
    '''Form that uses built-in UserCreationForm to handel user creation
    '''
    first_name = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(attrs={'placeholder': '*Jean..'}))
    last_name = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(attrs={'placeholder': '*Smith..'}))
    username = forms.EmailField(
        max_length=254, required=True,
        widget=forms.TextInput(attrs={'placeholder': '*Email..'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': '*Mot de passe..', 'class': 'password'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': '*Confirmer le mot de passe..',
                   'class': 'password'}))

    class Meta:
        """Class behaviour.
        """
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'password1', 'password2', )


class AuthForm(AuthenticationForm):
    '''Form that uses built-in AuthenticationForm to handel user auth
    '''
    username = forms.EmailField(
        max_length=254, required=True,
        widget=forms.TextInput(attrs={'placeholder': '*Email..'}))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': '*Mot de passe..', 'class': 'password'}))

    class Meta:
        """Class behaviour.
        """
        model = User
        fields = ('username','password', )


class UserProfileForm(forms.ModelForm):
    '''Basic model-form for our user profile that extends Django user model.
    '''
    telephone = forms.CharField(
        max_length=15, required=True,
        widget=forms.TextInput(attrs={'placeholder': '*Téléphone..'}))
    address = forms.CharField(
        max_length=100, required=True,
        widget=forms.TextInput(
            attrs={'placeholder': '*Adresse..'}))
    town = forms.CharField(
        max_length=100, required=True,
        widget=forms.TextInput(attrs={'placeholder': '*Ville..'}))
    county = forms.CharField(
        max_length=100, required=True,
        widget=forms.TextInput(attrs={'placeholder': '*Région..'}))
    post_code = forms.CharField(
        max_length=8, required=True,
        widget=forms.TextInput(attrs={'placeholder': '*Code Postale..'}))
    country = forms.CharField(
        max_length=100, required=True,
        widget=forms.Select(attrs={"class": "selection"}, choices=COUNTRIES))

    class Meta:
        """Class behaviour.
        """
        model = UserProfile
        fields = ('telephone', 'address', 'town', 'county',
                  'post_code', 'country')


class RequestPasswordForm(PasswordResetForm):
    '''Form that uses built-in PasswordResetForm to handel a request to
    reset password
    '''
    email = forms.EmailField(
        max_length=254, required=True,
        widget=forms.TextInput(attrs={'placeholder': '*Email..'}))

    class Meta:
        """Class behaviour.
        """
        model = User
        fields = ('email',)


class ForgottenPasswordForm(SetPasswordForm):
    '''Form that uses built-in SetPasswordForm to handel resetting passwords
    '''
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': '*Mot de passe..', 'class': 'password'}))
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': '*Confirmez votre mot de passe..',
                   'class': 'password'}))

    class Meta:
        """Class behaviour.
        """
        model = User
        fields = ('password1', 'password2', )


class TwoStepForm(forms.ModelForm):
    '''Basic model-form to enable 2-step auth
    '''
    two_step_code = forms.CharField(
        max_length=6, required=True,
        widget=forms.TextInput(attrs={'placeholder': '*Code..'}))

    class Meta:
        """Class behaviour.
        """
        model = UserToken
        fields = ('two_step_code',)
