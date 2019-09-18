from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, RegistrationForm, EditProfileForm
from .models import CustomUserModel, Contact
from actions.utils import create_action
from actions.models import Action
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
# Create your views here.


def user_login(request):
    if request.user.is_authenticated:
        return redirect("/dashboard")
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Login Success')
                    return redirect('/account')
                else:
                    return HttpResponse("Disabled Account")
            else:
                return HttpResponse("Invalid Login")
    else:
        form = LoginForm()
    context = {
        'form'  :   form,
    }
    return render(request, 'account/login.html', context)

def user_logout(request):
    logout(request)
    return render(request, "account/logout.html", {})

def user_signup(request):
    if request.user.is_authenticated:
        return redirect("/dashboard")
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            create_action(new_user, "has created an account")
            return render(request, "account/signup_done.html", {'new_user' : new_user})
    else:
        form = RegistrationForm()
    context = {
        'form'  :   form,
    }
    return render(request, "account/signup.html", context)

@login_required
def dashboard(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)
    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user').prefetch_related('target')[:10]
    context = {
        'section' : 'dashboard',
        'actions' : actions,
    }
    return render(request, "account/dashboard.html", context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/account")
    else:
        form = EditProfileForm(instance=request.user)
    context = {
        'form' : form,
    }
    return render(request, "account/edit_profile.html", context)

@login_required
def user_list(request):
    users = CustomUserModel.objects.filter(is_active=True)
    return render(request, "account/list.html", {'section':'people', 'users':users})

@login_required
def user_detail(request, username):
    user = get_object_or_404(CustomUserModel, username=username, is_active=True)
    return render(request, "account/detail.html", {'section':'people', 'user':user})

@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action  = request.POST.get('action')
    if user_id and action:
        try:
            user = CustomUserModel.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, "is following", user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except CustomUserModel.DoesNotExist:
            return JsonResponse({'status':'ko'})
    return JsonResponse({'status':'ko'})
