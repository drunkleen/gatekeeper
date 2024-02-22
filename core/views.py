from urllib.parse import urljoin

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
from django.contrib import messages
from core.models import UserAccount, Subscription
from core.forms import UserCreationForm, AdminUserCreationForm, AdminUserEditForm, UserEditForm, UserPasswordChangeForm


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
            return redirect('panel-user', username=request.user.username)
    return redirect('sign-in')


def user_sign_in(request) -> render:
    if request.user.is_authenticated:
        if request.user.account_type in ('admin', 'moderator'):
            return redirect('panel-admin')
        return redirect('panel-user', username=request.user.username)

    context = {
        'page_title': ['Sign In'],
    }
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = UserAccount.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                if user.account_type in ('admin', 'moderator'):
                    return redirect('panel-admin')
                return redirect('panel-user', username=user.username)

        except ObjectDoesNotExist:
            messages.error(request, 'Invalid email or password')

    if 'logout' in request.GET and request.GET['logout'] == '1':
        messages.success(request, 'You have successfully logged out.')

    return render(request, 'sign-in.html', context)


def user_sign_up(request) -> render:
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():

            user_form = form.save(commit=False)
            user_form.account_type = 'user'
            user_form.first_name = user_form.first_name.capitalize()
            user_form.last_name = user_form.last_name.capitalize()
            user_form.email = user_form.email.lower()
            user_form.username = user_form.username.lower()
            form.save()

            login(request, user_form)

            return redirect('panel-user', username=request.user.username)

    context = {
        'page_title': ['Sign Up'],
    }
    form = UserCreationForm()
    context['form'] = form
    return render(request, 'sign-up.html', context)


def user_sign_out(request) -> redirect:
    logout(request)
    return redirect('sign-in')


@login_required(login_url='/auth/sign-in')
def panel_admin(request) -> render:
    if request.user.account_type in ('admin', 'moderator'):
        context = {
            'request': request,
            'page_title': ['User Management', 'Overview'],
        }
        return render(request, 'panel/components/page/overview.html', context)


@login_required(login_url='/auth/sign-in')
def panel_admin_user_list(request) -> render:
    if request.user.account_type in ('admin', 'moderator'):
        context = {
            'request': request,
            'page_title': ['User Management', 'User List'],
        }

        page_ordering = request.GET.get('order', '-id')

        if request.user.account_type == 'admin':
            users = UserAccount.objects.all().order_by(f'{page_ordering}')
        else:
            users = UserAccount.objects.filter(account_type='user').order_by(f'{page_ordering}')

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
        return HttpResponse("404")


@login_required(login_url='/auth/sign-in')
def panel_admin_edit_user(request, username: str) -> render:
    if request.user.account_type in ['admin', 'moderator']:

        context = {
            'request': request,
            'page_title': ['User Management', 'User Setting', 'User Settings'],
        }

        user = get_object_or_404(UserAccount, username=username)

        if request.method == 'POST':
            form = AdminUserEditForm(request.POST, instance=user)
            if form.is_valid():
                user_form = form.save(commit=False)
                user_form.email = user_form.email.lower() \
                    if user_form.email != "" else user_form.email
                user_form.username = user_form.username.lower() \
                    if user_form.username != "" else user_form.username
                user_form.first_name = user_form.first_name.capitalize() \
                    if user_form.first_name != "" else user_form.first_name
                user_form.last_name = user_form.last_name.capitalize() \
                    if user_form.last_name != "" else user_form.last_name
                user_form.save()

        form = AdminUserEditForm(instance=user)
        context['form'] = form
        return render(request, 'panel/components/page/admin-edit-user.html', context)

    return redirect('sign-in')


@login_required(login_url='/auth/sign-in')
def panel_admin_delete_user(request, username: str) -> redirect:
    if request.user.account_type == ('admin' or 'moderator'):

        user = UserAccount.objects.get(username=username)

        if request.user.account_type == 'admin':
            user.delete()
            return redirect('panel-admin-user-lists')

        if request.user.account_type == 'moderator' and user.account_type == 'user':
            user.delete()
            return redirect('panel-admin-user-lists')

    return error_403(request, username)


@login_required(login_url='/auth/sign-in')
def panel_user_profile_overview(request, username: str) -> render:
    context = {
        'request': request,
    }

    if request.user.username == username:
        user = get_object_or_404(UserAccount, username=username)
        context['page_title'] = ['Users', 'Profile', 'User Profile']
        context['user'] = user

        return render(request, 'panel/components/page/user-profile.html', context)

    return redirect('sign-in')


@login_required(login_url='/auth/sign-in')
def panel_user_edit(request, username: str) -> render:
    if request.user.username == username:
        context = {
            'request': request,
            'page_title': ['Users', 'Profile', 'User Settings']
        }

        user = get_object_or_404(UserAccount, username=username)

        if request.method == 'POST':
            form = UserEditForm(request.POST, instance=user)
            if form.is_valid():
                user_form = form.save(commit=False)
                user_form.email = user_form.email.lower() \
                    if user_form.email != "" else user_form.email
                user_form.username = user_form.username.lower() \
                    if user_form.username != "" else user_form.username
                user_form.first_name = user_form.first_name.capitalize() \
                    if user_form.first_name != "" else user_form.first_name
                user_form.last_name = user_form.last_name.capitalize() \
                    if user_form.last_name != "" else user_form.last_name
                user_form.save()

                return redirect('panel-user-profile', username=user_form.username)

        context['form'] = AdminUserEditForm(instance=user)
        context['password_reset_form'] = UserPasswordChangeForm(user)
        return render(request, 'panel/components/page/edit-user.html', context)

    return redirect('sign-in')


@login_required(login_url='/auth/sign-in')
def panel_user_reset_password(request, username: str) -> redirect:
    user = get_object_or_404(UserAccount, username=username)

    if request.method == 'POST':
        form = UserPasswordChangeForm(user, request.POST)

        if form.is_valid() and user.check_password(form.cleaned_data['old_password']):
            if (
                    request.user.account_type == 'admin' or
                    (request.user.account_type == 'moderator' and user.account_type == 'user') or
                    (request.user.account_type == 'moderator' and user.username == request.user.username) or
                    user.username == request.user.username
            ):
                form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')

        return redirect('edit-user', username=username)

    messages.error(request, 'Action Not Allowed')
    return redirect('edit-user', username=username)


@login_required(login_url='/auth/sign-in')
def user_link_control(request, username: str) -> render:
    context = {

        'page_title': ['Link Control', 'View Links'],
        'request': request,
    }
    try:
        links = Subscription.objects.filter(assigned_to=request.user).filter(is_active=True)
        context['links'] = links
        context['exposed_links'] = links.filter(expose=True),
        context['restricted_links'] = links.filter(expose=False),
    except ObjectDoesNotExist:
        messages.error(request, 'No subscription links were located.')

    return render(request, 'panel/components/page/link-control.html', context)
