from django.shortcuts import  render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.template import context
from .forms import NewUserForm , ContactForm , CustomerForm
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import login, authenticate 
from django.contrib.auth import logout
from .decorators import unauthenticated_user
from django.contrib.auth.models import Group
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
# Create your views here.

from django.conf import settings


@unauthenticated_user
def index(request):
    form = NewUserForm()
    if request.method == 'POST':
        if 'register' in request.POST:
            print(request.POST,"REGISTER")
            form = NewUserForm(request.POST)
            if form.is_valid():
                print("VALID REG")
                user = form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f"New account created: {username}")
                group = Group.objects.get(name='customer')
                user.groups.add(group)
                login(request,user)
                messages.success(request,'You have been registered')
                return redirect('/')
            else:
                messages.error(request, "Unsuccessful registration. Invalid information.")
        elif 'login' in request.POST:
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                print("VALID LOGIN")
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}.")
                    return redirect("/")
                else:
                    messages.error(request,"Invalid username or password.")
            else:
                messages.error(request,"Invalid username or password.")
    return render(request,'users/login.html',{'form':form})

def logout_view(request):
    logout(request)
    return redirect('login')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email'], 
			    'message':form.cleaned_data['message'], 
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject,message,settings.EMAIL_HOST_USER,['guna19may2015@gmail.com'],fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('/')
    form = ContactForm()
    return render(request,'users/contact.html',{'form':form})


def account(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            user = request.user.customer
            context = {
                'user':user,
            }
            return render(request,'users/account.html' , context)
        elif request.method == 'POST':
            print("request.POST:", request.POST)
            customer_name = request.POST.get('customer_name')
            customer_email = request.POST.get('email')
            customer_mobile = request.POST.get('number')
            address = request.POST.get('address')
            city = request.POST.get('acc-city')
            state = request.POST.get('acc-state')
            zipcode = request.POST.get('acc-zip')
            country = request.POST.get('acc-country')
            user = request.user.customer
            user.customer_name = customer_name
            user.customer_email = customer_email
            user.customer_mobile = customer_mobile
            user.address = address
            user.city = city
            user.state = state
            user.zipcode = zipcode
            user.country = country
            user.save()
            return redirect('account')
    return render(request,'users/account.html')
