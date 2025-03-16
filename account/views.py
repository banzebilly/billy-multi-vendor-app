from django.shortcuts import render, redirect
from django.contrib import messages, auth
from .models import UserAccount, UserProfile
from .forms import UserAccountForm
from vendor_app.forms import VendorForm
from .utils import detect_User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

from django.http.response import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from .utils import detect_User, send_verification_email

from vendor_app.models import Vendor
from django.template.defaultfilters import slugify


#restrict vendor from accessing the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise  PermissionDenied   

#restrict customer from accessing the customer page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise   PermissionDenied
#----------------------------REGISTER FUNCTION START HERE---------------------------------------------------------
def register_User(request):
    if request.user.is_authenticated:
        messages.warning(request, 'you re already logged in')
        return redirect('myAccount')

    elif request.method == 'POST':
        form = UserAccountForm(request.POST)
        if form.is_valid():
            
            #================this is one way of creating a user using form=======================================
            #if you want to hash the password
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)#that s how we assigning the user before we save the data
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()
            #=this is other way of creating a user using create_user method =======================================
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = UserAccount.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = UserAccount.CUSTOMER
            user.save()

            #=========================email verification email==================================
            # mail_subject = 'Please activate your account'
            # email_template = 'acount/email/account_verification_email.html'
            send_verification_email(request, user)

            messages.success(request, 'WE HAVE SENT YOU THE LINK INTO YOUR EMAIL ADDRESS TO ACTIVATE YOUR ACCOUNT!')
            return redirect('register_User')
           
        else:
            # This will print the errors if the form is invalid
            print(form.errors)
            messages.error(request, 'There was an error with your submission. Please check the form and try again.')
    else:
        form = UserAccountForm()

    context = {
        'form': form,
    }
    return render(request, 'account/register.html', context)

 

#==========================================Register Vendor start here===============================================================
def register_vendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'you re already logged in')
        return redirect('myAccount')
        
    elif  request.method == 'POST':
        form = UserAccountForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if  form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = UserAccount.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = UserAccount.VENDOR
            user.save()
            #vendor 
            vendor = v_form.save(commit=False)
            #we need to provide vender profile , user
            vendor.user = user

            vendor_name = v_form.cleaned_data['vendor_name']
            vendor.vendor_slug = slugify(vendor_name)+'-'+str(user.id)
            #we do not have user_profile let get it signal will create user profile
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            vendor.user_profile = user_profile
            vendor.save()

             # ==================Send verification email to vendor user================
            send_verification_email(request, user)
            # mail_subject = 'Please activate your account'
            # email_template = 'acount/email/account_verification_email.html'
            # send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, 'your account has been registered successfully, Please wait for the approval')
            return redirect('register_vendor')

        else:
            print(form.errors)    


       
    else:
        form = UserAccountForm()
        #for vendor
        v_form = VendorForm()

    context = {
        'form': form,
        'v_form': v_form,
    }
    return render(request, 'account/register_vendor.html', context)

#===============account activation start here=============================================
def activate(request, uidb64, token):
    # Activate the user by setting the is_active status to True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserAccount._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, UserAccount.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulation! Your account is activated.')
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('myAccount')
        


#========================forgot password view start here===========================
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # send reset password email
            mail_subject = 'Reset Your Password'
            email_template = 'account/email/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, 'Password reset link has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgot_password')
    return render(request, 'account/forgot_password.html')
    
#reset password validator views start here ================================================
def reset_password_validate(request, uidb64, token):
    # validate the user by decoding the token and user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('myAccount')

#reset password views start here============================================================
def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('reset_password')
    return render(request, 'account/reset_password.html')





#----------------------------LOGIN FUNCTION START HERE---------------------------------------------------------

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'you re already logged in')
        return redirect('dashboard')

    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']


        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.info(request, 'your a logged in ')
            return redirect('myAccount')
        else:
            messages.error(request, 'invalid login credentials')  
            return redirect('login')  

    return render(request, 'account/login.html')   

#----------------------------LOGOUT FUNCTION START HERE---------------------------------------------------------
def logout(request):
    auth.logout(request)
    messages.info(request, 'your re logged out')  
    return redirect('login')

#----------------------------ACCOUNT FUNCTION  START HERE---------------------------------------------------------
#this my account will help us to identify  wether the person is customer or vendor the 
@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirect_url = detect_User(user)
    return redirect( redirect_url)

#----------------------------CUSTOMER DASHBOARD START HERE---------------------------------------------------------
@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customer_dashboard(request):

    return render(request, 'account/customer_dashboard.html')
    
#----------------------------VENDOR DASHBOARD START HERE---------------------------------------------------------
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendor_dashboard(request):
    #write the code to fetch the vendor profile detail
    # vendor = Vendor.objects.get(user=request.user)
    # context = {
    #     'vendor': vendor,
    # }
   
    return render(request, 'account/vendor_dashboard.html')