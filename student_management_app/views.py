# from channels.auth import login, logout
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from student_management_app.UsernameBackEnd import UsernameBackEnd

from student_management_system.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives, BadHeaderError, send_mail
import smtplib


from student_management_app.models import student


def home(request):
    return render(request, 'index.html')


def loginPage(request):
    return render(request, 'login.html')

def pitlogin(request):
    return render(request, 'PIT.html')

def sample(request):
    return render(request, 'sample.html')

def pages(request):
    return render(request, 'pages.html')



def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = UsernameBackEnd.authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            usertype=request.POST.get('usertype')
            user_type = user.user_type
            #return HttpResponse("Email: "+request.POST.get('email')+ " Password: "+request.POST.get('password'))
            if user_type == '1'== usertype:
                return redirect('admin_home')
                
            elif user_type == '2' == usertype:
                # return HttpResponse("Staff Login")
                return redirect('staff_home')
                
            elif user_type == '3' == usertype:
                # return HttpResponse("Student Login")
                return redirect('student_home')
            elif user_type == '4' == usertype:
                # return HttpResponse("Student Login")
                return redirect('student_home')
            else:
                messages.error(request, "Invalid Login!")
                return redirect('login')
        else:
            messages.error(request, "Invalid Login Credentials!")
            #return HttpResponseRedirect("/")
            return redirect('login')



def get_user_details(request):
    if request.user != None:
        return HttpResponse("User: "+request.user.username+" User Type: "+request.user.user_type)
    else:
        return HttpResponse("Please Login First")



def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

def send_email(request):
    recievers = []
    for s in student.objects.all():
        recievers.append(student.EMAIL)

    send_mail('PIT BSInfoTech Student Curriculum Residency Update',
        f'Hello {student.FIRSTNAME},\n Please check your current status at www.wapata.com', 
        EMAIL_HOST_USER,
        recievers,
        fail_silently=False)

    return render(request, "hod_template/send_email.html",context)