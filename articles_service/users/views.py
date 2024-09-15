from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages

def register_page(request):
    return render(request, 'registration/register.html')

@require_POST
def register(request):
    username = request.POST.get('login')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')

    if User.objects.filter(username=username).exists(): 
        messages.error(request, 'Пользователь с данным логином уже существует')
        return render(request, 'registration/register.html')

    if len(username) < 5:
        messages.error(request, 'Логин слишком короткий')
        if len(password1) < 5:
            messages.error(request, 'Пароль слишком короткий')
        return render(request, 'registration/register.html')
    
    if len(password1) < 5:
        messages.error(request, 'Пароль слишком короткий')
        return render(request, 'registration/register.html')
    
    if password1 != password2:
        messages.error(request, 'Пароли не сходятся')
        return render(request, 'registration/register.html')
    
    user = User.objects.create_user(username=username, password=password1)
    user.save()

    login(request, user)

    return redirect(reverse('home'))