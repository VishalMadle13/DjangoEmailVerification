from django.shortcuts import render,redirect
from django.views import View
from .forms import SignUpForm,SignInForm
from .models import Profile
from django.core.mail import send_mail
import uuid
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse

class Home(View):
    def get(self,request):
        return render(request,'home.html')
    
def send_mail_after_registration(email,token):
    subject = "Verify Email"
    message = f'Hi Click on the link to verify your account http://127.0.0.1:8000/account-verify/{token}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipient_list)

class SignUpView(View):
    def get(self,request):
        fm = SignUpForm()
        return render (request, 'sign-up.html' ,{'form' : fm})
        
    def post(self,request):
       try : 
            fm = SignUpForm(request.POST) 
            if fm.is_valid():
                uid = uuid.uuid4() 
                new_user = fm.save()  
                pro_obj  = Profile(user = new_user,token = uid)
                pro_obj.save() 
                send_mail_after_registration(new_user.email , uid) 
                messages.success(request,"your Account registered successfully, check your email and verify your account")
                return redirect('sign-in') 
            error = fm.errors
            messages.error(request,error)
            return redirect('sign-up')
       except Exception as e :
           return HttpResponse(e)

def account_verify(request,token):
        try :
            pf = Profile.objects.filter(token = token).first() 
            pf.verify = True
            pf.save()
            messages.success(request,"Your account is verified Successfully!! please Log in")
            return redirect('sign-in')
        except Exception as e :
             return HttpResponse("404 Error")
 
    
class SignInView(View):
     def get(self,request):
          fm = SignInForm()   
          return render(request,'sign-in.html',{'form' : fm})
     def post(self,request):
        try  : 
          fm = SignInForm(request, data = request.POST)
          if fm.is_valid():
             username = fm.cleaned_data['username']
             password = fm.cleaned_data['password']
             
             user = authenticate(username = username, password = password) 
             profile = Profile.objects.get(user = user) 
             if profile.verify :
                  login(request,user) 
                  messages.info(request,"You have successfully logged in!!")
                  return redirect('/')
             else :
                  messages.info(request,"Your account is not verified, please check your email and verify")
                  return redirect('sign-in')
          error = fm.errors
          messages.error(request,error)
          return redirect('sign-in')
        
        except Exception as e :
            return HttpResponse(e)

 
def logout_view(request): 
  if request.method == 'POST' or request.method == 'GET':
    logout(request)
    return redirect('/')