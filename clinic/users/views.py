from urllib import request
from django.shortcuts import render,redirect

from users.filters import AppointFilter

from .models import Appointments, Profile

from .forms import CreateAppointment, EditUserForm, SigninForm, SignupForm, UserProfileForm
from django.contrib.auth import login, authenticate,logout
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from django.urls import reverse
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage  
from datetime import datetime, timezone
from .tokens.token import TokenGenerator
from django.http import HttpResponse
# Create your views here.

#######sign up#########

def signup(request):  
    if request.method == 'POST':  
        form = SignupForm(request.POST)
        profile = UserProfileForm(request.POST,request.FILES)
        if form.is_valid() and profile.is_valid():  
            # save form in the memory not in database  
            user = form.save(commit=False)  
            user.is_active = False 
            user.save()
            uprofile=profile.save(commit=False)
            uprofile.user=user
            uprofile.save()
           
            # to get the domain of the current site  
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':TokenGenerator().make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
            return HttpResponse('Please confirm your email address to complete the registration')  
    else:  
        form = SignupForm()  
        profile= UserProfileForm()
    return render(request, 'signup.html', {'form': form,'profile':profile})  


def activate(request, uidb64, token):
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and TokenGenerator().check_token(user, token) and user.is_active == False: 
            print(user.date_joined)
            email_sent_at = user.date_joined
            now = datetime.now(timezone.utc)
            date_diffrince = (
               now-email_sent_at   
            ).seconds / 60
            print(date_diffrince)
            if date_diffrince < (24 * 60):
                user.is_active = True  
                user.save()
                return render(request,'confirmation.html')  
    else:  
        return HttpResponse('Activation link is invalid!')  
 
#######sign in#########

def signin_user(request):
    context={}
    if request.method=="POST":
     try:
        myform=SigninForm(request.POST)
        u = User.objects.get(email=request.POST['email'])
        user = authenticate(username=u.username,password=request.POST['password'])
        if u.is_active == True:
            login(request,user)     
            return redirect(reverse('users:homepage'))
        else:
            return HttpResponse('you should active your acount first... chick your Email')
     except:
         myform = SigninForm()
         context['form']=myform
         context['msg']='Wrong password or username ... '
         return render(request,'signin.html',context)
    else:
        myform = SigninForm()
        context['form']=myform
    return render(request,'signin.html',context)
#######logout#########
def logout_user(request):
    request.session.clear()
    logout(request)
    return redirect('users:signin')

#######user home page#########

def homepage(request):
 if (request.user.is_authenticated):
    user=User.objects.get(id=request.user.id)
    profile=Profile.objects.get(user=user)

    if request.method=='POST':
     form = CreateAppointment(request.POST)
     if form.is_valid():
      appoint=form.save(commit=False)
      appoint.user=user
      appoint.state='in processing'
      appoint.save() 
     return redirect(reverse('users:homepage'))
    else:
     if user.is_staff :
      appointments=Appointments.objects.all()
      myfilter= AppointFilter(request.GET,queryset=appointments)
      allappointments=myfilter.qs
      apointment_form=CreateAppointment()
      context={'user':user,'profile':profile,'appointments':allappointments,'form':apointment_form,'myfilter':myfilter}
     else: 
      allappointments=Appointments.objects.filter(user=user)
      apointment_form=CreateAppointment()
      context={'user':user,'profile':profile,'appointments':allappointments,'form':apointment_form}
    
    return render(request,'user_homepage.html',context)
 else:
     return redirect('users:signin')
 
#######appointment details#########
def appointment_details(request,id):
  if (request.user.is_authenticated):
    appointment=Appointments.objects.get(id=id)
    user=User.objects.get(id=request.user.id)
    profile=Profile.objects.get(user=user)
    context={'appointment':appointment,'user':user,'profile':profile}
    return render(request,'appointment_details.html',context)
  else:
     return redirect('users:signin')
#######cancel appointment #########
def appointment_cancel(request,id):
  if (request.user.is_authenticated):
    appointment=Appointments.objects.get(id=id)
    appointment.state='canceld'
    appointment.save()
    return redirect(reverse('users:homepage'))
  else:
     return redirect('users:signin')
 #######updat appointment #########
def appointment_update(request,id):
  if (request.user.is_authenticated):
    user=User.objects.get(id=request.user.id)
    appointment=Appointments.objects.get(id=id)
    profile=Profile.objects.get(user=user)
    if request.method =="POST":
        form=CreateAppointment(request.POST)
        if form.is_valid():
          appointment.state='reschedule'
          appointment.date=request.POST['date']
          appointment.time=request.POST['time']
          appointment.save()
        return redirect(reverse('users:homepage'))
    else:
        form=CreateAppointment()
        context={'user':user,'profile':profile,'appointments':appointment,'form':form}
        return render(request,'appointment_update.html',context)
  else:
     return redirect('users:signin')
 
 #######approved appointment #########
def appointment_approved(request,id):
   if (request.user.is_authenticated):
    appointment=Appointments.objects.get(id=id)
    appointment.state='approved'
    appointment.save()
    return redirect(reverse('users:homepage'))
   else:
     return redirect('users:signin')
  ####### appointment canceld_by_admin #########
def appointment_canceld_by_admin(request,id):
   if (request.user.is_authenticated):
    appointment=Appointments.objects.get(id=id)
    appointment.state='canceld by doctor'
    appointment.save()
    return redirect(reverse('users:homepage'))
   else:
    return redirect('users:signin')