"""Views module.
"""
import json
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from orders.models import Order

from .models import UserToken
from .mixins import (
    form_errors,
    redirect_params,
    TokenGenerator,
    ActivateTwoStep,
    CreateEmail)
from .forms import (
    UserForm,
    UserProfileForm,
    ForgottenPasswordForm,
    AuthForm,
    RequestPasswordForm,
    TwoStepForm)

MESSAGE = "Un incident est survenu. Vérifiez et réessayez !"
ERR = "error"
OK = "perfect"


def sign_up(request):
    '''Basic view for user sign up
    '''
    # Redirect if user is already signed in
    if request.user.is_authenticated:
        return redirect(reverse('users:sign-up'))

    user_form = UserForm()
    userprofile_form = UserProfileForm()
    result = ERR
    message = MESSAGE
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    # Safe guard to stop sign up until API key is added
    if settings.TWILIO_TOKEN == "XXX":
        return HttpResponse(
            json.dumps({"result": result, "message": message}),
            content_type="application/json")

    if is_ajax and request.method == "POST":
        user_form = UserForm(data=request.POST)
        userprofile_form = UserProfileForm(data=request.POST)

        # If both forms are valid, do something
        if user_form.is_valid() and userprofile_form.is_valid():
            user = user_form.save()

            # Commit = False is used as userprofile.user can not be null
            userprofile = userprofile_form.save(commit=False)
            userprofile.user = user
            userprofile.save()

            # Mark user profile as inactive until verified
            user.is_active = False
            user.email = user.username
            user.save()

            # Create a new token
            token = TokenGenerator()
            make_token = token.make_token(user)
            url_safe = urlsafe_base64_encode(force_bytes(user.pk))

            # Create and sends a SMS code
            sms_code = ActivateTwoStep(user=user, token=make_token)

            result = OK
            message = "Nous vous avons envoyé un SMS."
            context = {
                "result": result,
                "message": message,
                "url_safe": url_safe,
                "token": make_token
                }
        else:
            message = form_errors(user_form, userprofile_form)
            context = {"result": result, "message": message}

        return HttpResponse(
            json.dumps(context),
            content_type="application/json")

    context = {'u_form': user_form, 'up_form': userprofile_form}
    return render(request, 'users/sign_up.html', context)


def sign_in(request):
    '''Basic view for user sign in.
    '''
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    # Redirect if user is already signed in
    if request.user.is_authenticated:
        return redirect(reverse('users:account'))

    auth_form = AuthForm()
    result = ERR
    message = MESSAGE

    if is_ajax and request.method == "POST":
        auth_form = AuthForm(data=request.POST)
        if auth_form.is_valid():
            username = auth_form.cleaned_data.get('username')
            password = auth_form.cleaned_data.get('password')
            # Authenticate Django built in authenticate -
            # https://docs.djangoproject.com/en/3.1/ref/contrib/auth/
            user = authenticate(request, username=username, password=password)

            if user is not None:

                # Check to see if 2-step verification is active
                if user.userprofile.two_step_active:
                    # Create and sends a SMS code
                    token = TokenGenerator()
                    make_token = token.make_token(user)
                    url_safe = urlsafe_base64_encode(force_bytes(user.pk))
                    # Create and sends a SMS code
                    sms_code = ActivateTwoStep(user=user, token=make_token)
                    message = 'Nous vous avons envoyé un SMS'
                    result = OK
                    return HttpResponse(
                        json.dumps(
                            {"result": result,
                             "message": message,
                             "url_safe": url_safe,
                             "token": make_token}),
                        content_type="application/json")

                login(request, user)
                message = 'Vous êtes connecté'
                result = OK

        else:
            message = form_errors(auth_form)

        return HttpResponse(
            json.dumps({"result": result, "message": message}),
            content_type="application/json")

    context = {'a_form': auth_form}

    # Passes 'token_error' parameter to url to handle a error message
    token_error = request.GET.get("token_error", None)

    if token_error:
        context["token_error"] = "true"
    else:
        context["token_error"] = "false"

    return render(request, 'users/sign_in.html', context)


def sign_out(request):
    '''Basic view for user sign out.
    '''
    logout(request)
    return redirect(reverse('users:sign-in'))


def forgotten_password(request):
    '''Basic view for users to request a new password.
    '''
    rp_form = RequestPasswordForm()
    result = ERR
    message = MESSAGE
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    if is_ajax and request.method == "POST":
        rp_form = RequestPasswordForm(data=request.POST)

        if rp_form.is_valid():
            username = rp_form.cleaned_data.get('email')
            user = User.objects.get(username=username)
            # Create a new token
            token = TokenGenerator()
            make_token = token.make_token(user)

            user_token = UserToken.objects.create(
                user=user,
                token=make_token,
                is_password=True)

            # Send email verification email
            CreateEmail(
                request,
                email_account="donotreply",
                subject='Réinitialisation de votre mot de passe',
                email=user.username,
                cc=[],
                template="mail/password_email.html",
                token=make_token,
                url_safe=urlsafe_base64_encode(force_bytes(user.pk))
            )
            result = OK
            message = "Vous allez recevoir un mail pour réinitialiser " \
                      "votre mot de passe."
        else:
            message = form_errors(rp_form)

        return HttpResponse(
            json.dumps({"result": result, "message": message}),
            content_type="application/json")
    context = {'rp_form': rp_form}
    return render(request, 'users/forgotten_password.html', context)


@login_required
def account(request):
    '''Account view for registered users
    '''
    if request.method == "POST":
        toggle = request.POST.get("toggle")
        userprofile = request.user.userprofile

        if toggle == "on":
            userprofile.two_step_active = True
        else:
            userprofile.two_step_active = False

        userprofile.save()

        return HttpResponse(
            json.dumps({}),
            content_type="application/json")

    context = {}
    # TODO add an owner to Coupon model and add it to the context to
    # display it in the account template.
    # Passes 'verified' parameter to url to handle a success message
    verified = request.GET.get("verified", None)

    order_query = Order.objects.filter(email=request.user.email)
    context = {'invoices': order_query}

    if verified:
        context["verified"] = "true"
    else:
        context["verified"] = "false"

    return render(request, 'users/account.html', context)


@login_required
def email(request):
    '''AJAX function to request email view for registered users.
    '''
    result = ERR
    message = MESSAGE

    if request.method == "POST":
        user = request.user
        # Create a new token
        token = TokenGenerator()
        make_token = token.make_token(user)
        url_safe = urlsafe_base64_encode(force_bytes(user.pk))

        # Create a usertoken object to store token
        user_token = UserToken.objects.create(
            user=user,
            token=make_token,
            is_email=True)

        # Send email verification email
        CreateEmail(
            request,
            email_account="donotreply",
            subject='Vérifiez votre email',
            email=user.username,
            cc=[],
            template="mail/verification_email.html",
            token=make_token,
            url_safe=url_safe)

        result = OK
        message = "Nous vous avons envoyé un mail de vérification."
        return HttpResponse(
            json.dumps({"result": result, "message": message}),
            content_type="application/json")

    return HttpResponse(
        json.dumps({"result": result, "message": message}),
        content_type="application/json")


def verification(request, uidb64, token):
    '''Function view to handle verification tokens
    '''
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        user_token = UserToken.objects.get(user=user,
                                           token=token,
                                           is_active=True)
        email_token = user_token.is_email
        password_token = user_token.is_password
    except (TypeError, ValueError, OverflowError,
            User.DoesNotExist, UserToken.DoesNotExist):
        # User our redirect_params function to redirect & append
        # 'token_error' parameter to fire an error message
        return redirect_params(url='users:sign-in',
                               params={"token_error": "true"})

    # If User & UserToken exist...
    if user and user_token:

        # If the token type is_email
        if email_token:
            # Deactivate the token now that it has been used
            user_token.is_active = False
            user_token.save()
            user_profile = user.userprofile
            user_profile.email_verified = True
            user_profile.save()
            # Login the user
            login(request, user)

            # User our redirect_params function to redirect & append 'verified'
            # parameter to fire a success message
            return redirect_params(url='users:account',
                                   params={"verified": "true"})

        # if the token is a password token
        is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

        if password_token:
            fp_form = ForgottenPasswordForm(user=user)
            result = ERR
            message = MESSAGE

            if is_ajax and request.method == "POST":
                fp_form = ForgottenPasswordForm(data=request.POST, user=user)

                if fp_form.is_valid():
                    fp_form.save()
                    login(request, user)

                    # Deactivate the token now that it has been used
                    user_token.is_active = False
                    user_token.save()
                    message = "Votre mot de passe a été réinitialisé."
                    result = OK
                else:
                    message = form_errors(fp_form)

                return HttpResponse(
                    json.dumps({"result": result, "message": message}),
                    content_type="application/json")
            context = {'fp_form': fp_form, "uidb64": uidb64, "token": token}
            return render(request, 'users/verification.html', context)

        # Else the token is for 2 step verification
        ts_form = TwoStepForm()
        result = ERR
        message = MESSAGE

        if is_ajax and request.method == "POST":
            ts_form = TwoStepForm(data=request.POST)

            if ts_form.is_valid():
                two_step_code = ts_form.cleaned_data.get('two_step_code')

                if two_step_code == user_token.two_step_code:
                    user.is_active = True
                    user.save()

                    login(request, user)

                    # Deactivate the token now that it has been used
                    user_token.is_active = False
                    user_token.save()
                    message = "Succès ! Vous êtes maintenant connecté."
                    result = OK
                else:
                    message = "Code incorrect, veuillez réessayer."
            else:
                message = form_errors(ts_form)

            return HttpResponse(
                json.dumps({"result": result, "message": message}),
                content_type="application/json")
        context = {'ts_form': ts_form, "uidb64": uidb64, "token": token}

        return render(request, 'users/two_step_verification.html', context)
