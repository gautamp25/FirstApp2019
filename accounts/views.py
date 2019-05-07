from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from contacts.models import Contact

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

def register(request):
    if request.method == 'POST':
        #Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        #Check validation
        if password == password2:
            #check username
            if User.objects.filter(username=username).exists():
                messages.error(request,'Sorry,that username is already taken.')
                return redirect('register')
            else:#check email    
                if User.objects.filter(email=email).exists():
                    messages.error(request,'Sorry,that email is already exists.')
                    return redirect('register') 
                else:
                    # all good
                    user = User.objects.create_user(username=username, email=email, password=password, 
                    first_name=first_name, last_name=last_name)
                    #Login after register
                    # auth.login(request,user)
                    # messages.success(request,'You are logged in now')
                    # return redirect('index')
                    user.save()
                    messages.success(request,'Your Registration Successful')
                    return redirect('login')
        else:
            messages.error(request,'Password do not match.')
            return redirect('register')     
    else:
        return render(request, 'accounts/register.html')  

def dashboard(request):
    user_contact = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context = {
        'contacts':user_contact
    }
    return render(request, 'accounts/dashboard.html',context) 

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request,'You are now logged out.')
        return redirect('index')     
