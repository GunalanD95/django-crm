from django.shortcuts import  render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import NewUserForm

# Create your views here.


def index(request):
    form = NewUserForm()
    if request.method == 'POST':
        print(request.POST,"REGISTER")
        form = NewUserForm(request.POST)
        if form.is_valid():
            print("VALID")
            user = form.save()
            login(request,user)
            messages.success(request,'You have been registered')
            return redirect('home')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")  
    return render(request,'users/login.html',{'form':form})

