from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from . models import Record

# Create your views here.
def home(request):
    records = Record.objects.all()
    context = {
        'records': records,
    }

    # check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in.")
            return redirect('home')
        else:
            messages.success(request, "There was an error logging in.")
            return redirect('home')    
    else:
        return render(request, 'home.html', context=context)

def logout_user(request):
    logout(request)   
    messages.success(request, "You have been logged out.")   
    return redirect('home')  

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have been registered.")
            return redirect('home')
    else:
        form = SignUpForm()    
        context = {
            'form': form,
        }    
        return render(request, 'register.html', context=context)

    return render(request, 'register.html', context=context)   

def customer_record(request, pk):
    if request.user.is_authenticated:
        #Look up records
        customer_record = Record.objects.get(id=pk) 
        context = {
            'customer_record': customer_record,
        } 
        return render(request, 'record.html', context=context)
    else:
        messages.success(request, "You must be logged in to view that page.")  
        return redirect('home')    

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "That record is successfully deleted.")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in to do that.")
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record added.")
                return redirect('home')
        context = {
            'form': form,
        }        
        return render(request, 'add_record.html', context=context)
    else:
        messages.success(request, "You must be logged in to do that.")
        return redirect('home')

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record has been updated.")
            return redirect('home')
        context = {
            'form': form,
            'current_record': current_record,
        }    
        return render(request, 'update_record.html', context=context)    
    else:
        messages.success(request, "You must be logged in to do that.")
        return redirect('home')    