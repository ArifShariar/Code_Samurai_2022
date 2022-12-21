from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from Projects.models import Project
from Users.forms import UserForm, ProfileForm
from Users.models import Profile




def default_home(request):
    projects = Project.objects.all()
    context = {'projects': projects}
    return render(request, 'homepage/default_home.html', context)


@login_required(login_url='login_user')
def home(request):
    user_id = request.user.id
    user_profile = Profile.objects.get(user_id=user_id)
    projects = Project.objects.all()
    context = {'projects': projects, 'profile': user_profile}
    return render(request, 'homepage/home.html', context)


def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    user_form = UserForm()
    profile_form = ProfileForm()

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('login_user')

    return render(request, 'auth/register.html', {'user_form': user_form, 'profile_form': profile_form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is incorrect')
    return render(request, 'auth/login.html')


@login_required(login_url='login_user')
def logout_user(request):
    logout(request)
    return redirect('login_user')
