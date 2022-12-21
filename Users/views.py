from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from Projects.models import Project
from Users.forms import UserForm, ProfileForm
from Users.models import Profile, User




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
            sys_admin = Profile.objects.filter(user_type='SYSADMIN').first()
            if sys_admin is None and profile_form.cleaned_data['user_type'] != 'SYSADMIN':
                messages.error(request, 'You must register a system admin first')
                return redirect('register_user')

            elif profile_form.cleaned_data['user_type'] == 'SYSADMIN' and sys_admin is not None:
                messages.error(request, 'System admin already exists')
                return redirect('register_user')

            elif profile_form.cleaned_data['user_type'] == 'SYSADMIN' and sys_admin is None:
                user = user_form.save()
                user.set_password(user.password)
                user.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
                messages.success(request, 'Account created successfully')
                return redirect('login_user')

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
            profile_user = Profile.objects.get(user_id=user.id)
            if profile_user.is_verified:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Your account is not verified')
                return redirect('login_user')
        else:
            messages.error(request, 'Username or Password is incorrect')
    return render(request, 'auth/login.html')


@login_required(login_url='login_user')
def logout_user(request):
    logout(request)
    return redirect('login_user')


@login_required(login_url='login_user')
def get_all_unverified_users(request):
    profile_id = Profile.objects.get(user_id=request.user.id)

    if profile_id.user_type == 'SYSADMIN':
        unverified_users = Profile.objects.filter(is_verified=False)
        context = {'unverified_users': unverified_users, 'profile': profile_id}
        return render(request, 'auth/unverified_users.html', context)
    else:
        print('You are not authorized to view this page')
        return redirect('home')


@login_required(login_url='login_user')
def approve_user(request, pk):
    profile_id = Profile.objects.get(user_id=request.user.id)
    if profile_id.user_type == 'SYSADMIN':
        user_ob = User.objects.get(id=pk)
        profile_ob = Profile.objects.get(user=user_ob)
        profile_ob.is_verified = True
        profile_ob.save()
        return redirect('unverified_user')
    else:
        print('You are not authorized to view this page')
        return redirect('home')


@login_required(login_url='login_user')
def decline_user(request, pk):
    profile_id = Profile.objects.get(user_id=request.user.id)
    if profile_id.user_type == 'SYSADMIN':
        user = User.objects.get(id=pk)
        user.delete()
        return redirect('unverified_user')
    else:
        print('You are not authorized to view this page')
        return redirect('home')
