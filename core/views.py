from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django import template

from core.models import UserAccount, Subscription
from core.forms import UserCreationForm, AdminUserCreationForm, AdminUserEditForm


# Create your views here.

# Error handling
def error_400(request, exception) -> render:
    context = {
        "pre_url": request.META.get('HTTP_REFERER'),
        "error": "400",
        "text": "Bad Request!",
    }
    return render(request, 'error_handlers/index.html', context)


def error_403(request, exception) -> render:
    context = {
        "pre_url": request.META.get('HTTP_REFERER'),
        "error": "403",
        "text": "Access denied!",
    }
    return render(request, 'error_handlers/index.html', context)


def error_404(request, exception) -> render:
    context = {
        "pre_url": request.META.get('HTTP_REFERER'),
        "error": "404",
        "text": "Page not found!",
    }
    return render(request, 'error_handlers/index.html', context)


def return_error(request, error_code: str, text: str) -> render:
    context = {
        "pre_url": request.META.get('HTTP_REFERER'),
        "error": error_code,
        "text": text,
    }
    return render(request, 'error_handlers/index.html', context)


def error_500(request) -> render:
    context = {
        "pre_url": request.META.get('HTTP_REFERER'),
        "error": "500",
        "text": "Internal Server Error!",
    }
    return render(request, 'error_handlers/index.html', context)


# View handler


def index(request) -> redirect:
    if request.user.is_authenticated:
        if request.user.account_type == 'admin' or request.user.account_type == 'moderator':
            return redirect('panel-admin')
        else:
            return HttpResponse("User")
    redirect('sign-in')


def user_sign_in(request) -> render:
    if request.user.is_authenticated:
        return HttpResponse('authenticated')

    context = {
        'page_title': 'Sign In',
    }
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if user.account_type == "admin" or user.account_type == "moderator":
                    return redirect('panel-admin')
                return redirect('panel-user')

        except UserAccount.DoesNotExist:
            messages.error(request, 'Invalid E-mail or password')

    return render(request, 'sign-in.html', context)


def user_sign_up(request) -> render:
    context = {
        'page_title': 'Sign Up',
    }

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print('\n\nform is valid')
            user = form.save(commit=False)
            user.account_type = 'user'
            user.first_name = user.first_name.capitalize()
            user.last_name = user.last_name.capitalize()
            user.email = user.email.lower()
            user.username = user.username.lower()
            form.save()

            login(request, user)
            return redirect('panel-user')

    form = UserCreationForm()
    context['form'] = form
    return render(request, 'sign-up.html', context)


def user_sign_out(request) -> redirect:
    logout(request)
    return redirect('sign-in')


def panel_admin(request):
    if request.user.is_authenticated and request.user.account_type == ('admin' or 'moderator'):
        context = {
            'request': request,
            'page_title': ['User Management', 'Overview'],
            'page_name': 'overview',
        }
        return render(request, 'panel/components/page/overview.html', context)


def panel_admin_user_list(request) -> render:
    if request.user.is_authenticated:
        context = {
            'request': request,
            'page_name': 'user list',
            'page_title': ['User Management', 'User Setting'],
        }

        if request.user.account_type == ('admin' or 'moderator'):
            page_num = request.GET.get('page', 1)
            page_ordering = request.GET.get('order', '-id')
            list_element_count = request.GET.get('count', 10)

            users = UserAccount.objects.all().order_by(f'{page_ordering}')[
                    ((page_num * list_element_count) - list_element_count):(page_num * list_element_count)
                    ]

            if request.method == 'POST':
                form = AdminUserCreationForm(request.POST)
                if form.is_valid():
                    user = form.save(commit=False)
                    user.email = user.email.lower()
                    user.username = user.username.lower()
                    form.save()

                    add_user_form = AdminUserCreationForm()
                    context['add_user_form'] = add_user_form
                    context['users'] = users
                    return render(request, 'panel/components/page/users-list.html', context)

            add_user_form = AdminUserCreationForm()
            context['add_user_form'] = add_user_form
            context['users'] = users

            return render(request, 'panel/components/page/users-list.html', context)
        else:
            context['page_title'] = 'User Panel'
            return render(request, 'panel/components/page/users-list.html', context)
    return redirect('sign-in')


def panel_admin_delete_user(request, username) -> render:
    if request.user.is_authenticated and request.user.account_type == ('admin' or 'moderator'):

        user = UserAccount.objects.get(username=username)

        if request.user.account_type == 'admin':
            user.delete()
            return panel_admin_user_list(request)

        if request.user.account_type == 'moderator' and user.account_type == 'user':
            user.delete()
            return redirect('panel-admin-user-lists')

    return error_403(request, username)


def panel_user_profile_overview(request, username):
    if request.user.is_authenticated:
        context = {
            'request': request,
            'page_name': 'user profile',
        }

        if request.user.account_type in ('admin', 'moderator') or request.user.username == username:
            user = get_object_or_404(UserAccount, username=username)
            context['page_title'] = ['Users', 'Profile', 'User Profile']
            context['user'] = user

            return render(request, 'panel/components/page/user-profile.html', context)

        return redirect('sign-in')

    return redirect('sign-in')


def panel_edit_user(request, username):
    if request.user.is_authenticated:
        context = {
            'request': request,
            'page_name': 'user setting',
        }

        if request.user.account_type in ('admin', 'moderator') or request.user.username == username:
            context['page_title'] = ['Users', 'Profile', ' User Setting']

            user = get_object_or_404(UserAccount, username=username)

            if request.method == 'POST':
                form = AdminUserEditForm(request.POST, instance=user)
                if form.is_valid():
                    user = form.save(commit=False)
                    user.email = user.email.lower()
                    user.username = user.username.lower()
                    user.first_name = user.first_name.capitalize()
                    user.last_name = user.last_name.capitalize()
                    form.save()

            form = AdminUserEditForm(instance=user)
            context['form'] = form
            return render(request, 'panel/components/page/edit-user.html', context)

        return redirect('sign-in')

    return redirect('sign-in')
