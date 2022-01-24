from django.shortcuts import  render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.template import context
from .forms import NewUserForm
from django.contrib.auth.forms import AuthenticationForm #add this
from django.contrib.auth import login, authenticate #add this
from django.contrib.auth import logout
from .decorators import unauthenticated_user
# Create your views here.

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
    return redirect('/')