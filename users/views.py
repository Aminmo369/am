from django.shortcuts import render , redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout , login ,authenticate
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


def logout_view(request):
    """خروج کاربر و هدایت به صفحه اصلی"""
    logout(request)
    return redirect(reverse('webchat:index'))

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_user = authenticate(username=user.username, password=request.POST['password1'])
            login(request, auth_user)  # ورود خودکار بعد از ثبت‌نام
            return redirect(reverse('webchat:index'))  # هدایت به صفحه اصلی
    else:
        form = UserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})