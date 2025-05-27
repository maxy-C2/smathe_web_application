from .tokens import generate_token
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.utils.encoding import force_bytes
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetConfirmView
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from smartWeatherProject import settings




# Create your views here.
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password_one = request.POST.get('pass1')
        password_two = request.POST.get('pass2')
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exists! Please try another one")
            return redirect('signup')

        if User.objects.filter(email=email):
            messages.error(request, "Email already exists")
            return redirect('signup')

        
        if len(username) > 30:
            messages.error(request, "Username must be under 30 characters long")
            return redirect('signup')

        
        if password_one != password_two:
            messages.error(request, "Passwords do not match")
            return redirect('signup')
        

        myuser = User.objects.create_user(username, email, password_one)
        myuser.is_active = False #is activated when link is clicked
        myuser.save()
        messages.success(request, "Your Account has been successfully created. We have sent a confirmation email. Check you email to confrim your account.")
        
        #sending Welcome email using smtp
        subject = "Welcome to the BlitzAgroTech Smart Weather Station Web Application"
        first_message = "Hello " + myuser.username + "\n" + "Welcome to BlitzAgroTech's Smart Weather Station Web Application. Thank you for visiting out site.\nPlease confirm your email address in order to activate your account.\n\nBest Regards,\nBlitzAgroTech Team."
        sender_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, first_message, sender_email, to_list, fail_silently=True)
        
        #sending confirmation email
        current_site = get_current_site(request)
        email_subject = 'Confirm your email @ BlitzAgroTech - Smart Weather Station Web Application'
        second_message = render_to_string(
            'email_confirmation.html', {
                'name': myuser.username, 
                'domain':current_site.domain, 
                'user_id': urlsafe_base64_encode(bytes(str(myuser.pk), 'utf-8')),
                'token': generate_token.make_token(myuser)
                }
            )
        
        send_mail(
            email_subject,
            second_message,
            settings.EMAIL_HOST_USER,
            [myuser.email],
            fail_silently = False 
        )
        
        return redirect('signin')
    

    return render(request, "signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('pass1')

        myuser = authenticate(username = username, email = email, password = password)

        if myuser is not None:
            login(request, myuser)
            return redirect('user_menu')
        
        else:
            messages.error(request, "InCorrect Credentials")
            return render(request, 'signin.html')

    return render(request, "signin.html")

def successful_activation(request):
    return render(request, 'successful_activation.html')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        myuser = User.objects.get(pk=uid)
        
    except (TypeError, OverflowError, User.DoesNotExist, ValueError):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect('successful_activation')
    else:
        messages.error(request, "Activation failed, please try again")
        return render(request, 'signin.html')
    


def terms(request):
    return render(request,'terms.html')


@csrf_protect
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            current_site = get_current_site(request)
            email_subject = 'Reset Your Password - BlitzAgroTech Smart Weather Station'
            reset_message = render_to_string(
                'password_reset_email.html', {
                    'username': user.username,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                }
            )
            
            send_mail(
                email_subject,
                reset_message,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )
            
            messages.success(request, "Password reset instructions have been sent to your email.")
            return redirect('password_reset_done')
        except User.DoesNotExist:
            # We don't want to reveal which emails exist in our system
            messages.success(request, "Password reset instructions have been sent to your email if an account with that email exists.")
            return redirect('password_reset_done')
            
    return render(request, "forgot_password.html")


def password_reset_done(request):
    return render(request, "password_reset_done.html")



def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            if new_password != confirm_password:
                messages.error(request, "Passwords do not match")
                return render(request, 'password_reset_confirm.html', {'uidb64': uidb64, 'token': token})
                
            user.set_password(new_password)
            user.save()
            messages.success(request, "Your password has been reset successfully. You can now login with your new password.")
            return redirect('signin')
        return render(request, 'password_reset_confirm.html', {'uidb64': uidb64, 'token': token})
    else:
        messages.error(request, "The password reset link is invalid or has expired.")
        return redirect('forgot_password')
    

def signout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('signin')  # Redirect to signin page