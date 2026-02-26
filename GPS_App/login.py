from django.shortcuts import render, HttpResponse, redirect
from .models import user
from django.contrib.auth.hashers import check_password,make_password
from django.contrib import messages

def login(request):
    if request.method == "POST":
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        # demo_pass= make_password(password)
        #
        # user.objects.create_user(first_name='admin',last_name='admin',email =email,password= password,mobile='7600524348',image='demo.png',)


        try:
            user_check = user.objects.get(email=email)
            if user_check:
                if check_password(password, user_check.password):
                    user_session = {'user_id':user_check.id,'user_first_name':user_check.first_name,'user_last_name':user_check.last_name}
                    request.session['user'] = user_session
                    return redirect('map')
                else:
                    messages.error(request, 'Invalid Password.')
            else:
                messages.error(request, 'Invalid Email Id.')
        except user.DoesNotExist:
            messages.error(request, 'Invalid Login.')

    return render(request, 'login.html')

def logout(request):
    if 'user' in request.session:
        del request.session['user']
    return redirect('login')