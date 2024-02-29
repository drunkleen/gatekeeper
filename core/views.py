from urllib.parse import urljoin

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
from django.contrib import messages
from core.models import UserAccount, Subscription
from core.forms import UserCreationForm, AdminUserCreationForm, AdminUserEditForm, UserEditForm, UserPasswordChangeForm, \
    UserEmailChangeForm, SubscriptionForm, SubscriptionEditForm
from core.utils.utils import generate_qr_code, link_scraper
from django.utils import timezone
from datetime import timedelta


def index(request) -> HttpResponse:
    if request.user.is_authenticated:
        if request.user.account_type == 'admin' or request.user.account_type == 'moderator':
            return redirect('panel-admin')
        else:
            return redirect('panel-user', username=request.user.username)
    return redirect('sign-in')


def user_sign_in(request) -> HttpResponse:
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
                return redirect('user-view-links', username=user.username)

        except ObjectDoesNotExist:
            messages.error(request, 'Invalid email or password')

    if 'logout' in request.GET and request.GET['logout'] == '1':
        messages.success(request, 'You have successfully logged out.')

    return render(request, 'sign-in.html', context)


def user_sign_up(request) -> HttpResponse:
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


def user_sign_out(request) -> HttpResponse:
    logout(request)
    return redirect('sign-in')


@login_required(login_url='/auth/sign-in')
def panel_admin(request) -> HttpResponse:
    if request.user.account_type in ('admin', 'moderator'):
        context = {
            'request': request,
            'page_title': ['User Management', 'Overview'],
        }

        try:
            last_24_h = timezone.now() - timedelta(days=1)
            last_week = timezone.now() - timedelta(days=7)
            users = UserAccount.objects

            context['last_24_h_active_users_count'] = len(users.filter(last_login__gte=last_24_h))
            context['last_week_active_users_count'] = len(users.filter(last_login__gte=last_week))
            context['overall_active_users_count'] = len(users.filter(last_login__isnull=False))

        except UserAccount.DoesNotExist:
            pass

        return render(request, 'panel/components/page/overview.html', context)
    return redirect('panel-user', username=request.user.username)


@login_required(login_url='/auth/sign-in')
def panel_admin_user_list(request) -> HttpResponse:
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
def panel_admin_edit_user(request, username: str) -> HttpResponse:
    if request.user.account_type in ['admin', 'moderator']:

        context = {
            'request': request,
            'page_title': ['User Management', 'User List', 'Edit User'],
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

                messages.success(request, 'User was successfully updated!')
                return redirect('panel-admin-user-lists')

        form = AdminUserEditForm(instance=user)
        context['form'] = form
        return render(request, 'panel/components/page/admin-edit-user.html', context)

    messages.error(request, 'Action Not Allowed')
    return redirect('panel-user', username=request.user.username)


@login_required(login_url='/auth/sign-in')
def panel_admin_create_link(request, username: str) -> HttpResponse:
    if request.user.account_type in ['admin', 'moderator']:

        context = {
            'request': request,
            'page_title': ['User Management', 'User List', 'Create Link'],
        }

        user = get_object_or_404(UserAccount, username=username)

        if request.method == 'POST':
            form = SubscriptionForm(request.POST)
            if form.is_valid():
                link_form = form.save(commit=False)
                link_form.created_by = request.user
                link_form.assigned_to = user
                link_form.expose = False
                link_form.save()

                messages.success(
                    request, f'Link was successfully assigned to {user.first_name} {user.last_name} [{user.username}].'
                )
                return redirect('panel-admin-user-lists')

        form = SubscriptionForm()
        context['form'] = form
        context['user'] = user
        return render(request, 'panel/components/page/admin-create-link.html', context)

    messages.error(request, 'Action Not Allowed')
    return redirect('panel-user', username=request.user.username)


@login_required(login_url='/auth/sign-in')
def panel_admin_edit_link(request, shorten_uuid_link: str) -> HttpResponse:
    if request.user.account_type in ['admin', 'moderator']:

        context = {
            'request': request,
            'page_title': ['User Management', 'User List', 'Edit Link'],
        }

        link = get_object_or_404(Subscription, subscription_uuid=shorten_uuid_link)

        if request.method == 'POST':
            form = SubscriptionEditForm(request.POST, instance=link)
            if form.is_valid():
                link_instance = form.save(commit=False)
                link_instance.save()

                messages.success(
                    request,
                    f'Link with the id [{link.subscription_uuid}] was successfully updated.'
                )
                return redirect('user-view-links', username=link.assigned_to.username)

        form = SubscriptionEditForm(instance=link)
        context['form'] = form
        context['user'] = link.assigned_to
        return render(request, 'panel/components/page/admin-edit-link.html', context)

    messages.error(request, 'Action Not Allowed')
    return redirect('panel-user', username=request.user.username)


@login_required(login_url='/auth/sign-in')
def panel_admin_delete_user(request, username: str) -> HttpResponse:
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
def panel_user_profile_overview(request, username: str) -> HttpResponse:
    context = {
        'request': request,
    }

    if request.user.username == username:
        user = get_object_or_404(UserAccount, username=username)
        context['page_title'] = ['Users', 'Profile', 'User Profile']
        context['user'] = user
        context['form'] = AdminUserEditForm(instance=user)
        context['email_change_form'] = UserEmailChangeForm(instance=user)
        context['password_reset_form'] = UserPasswordChangeForm(user)

        return render(request, 'panel/components/page/user-profile.html', context)

    return redirect('sign-in')


@login_required(login_url='/auth/sign-in')
def panel_user_edit(request, username: str) -> HttpResponse:
    user = get_object_or_404(UserAccount, username=username)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            if (request.user.account_type == 'admin' or
                    (request.user.account_type == 'moderator' and user.account_type == 'user') or
                    (request.user.account_type == 'moderator' and user.username == request.user.username) or
                    user.username == request.user.username
            ):
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
                messages.success(request, 'Your Profile was successfully updated!')

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')

        return redirect('panel-user-profile', username=username)

    messages.error(request, 'Action Not Allowed')
    return redirect('panel-user-profile', username=username)


@login_required(login_url='/auth/sign-in')
def panel_user_change_email(request, username):
    user = get_object_or_404(UserAccount, username=username)

    if request.method == 'POST':
        form = UserEmailChangeForm(request.POST, instance=user)

        if form.is_valid():
            if (request.user.account_type == 'admin' or
                    (request.user.account_type == 'moderator' and user.account_type == 'user') or
                    (request.user.account_type == 'moderator' and user.username == request.user.username) or
                    user.username == request.user.username
            ):
                form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your E-mail was successfully updated!')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')

        return redirect('panel-user-profile', username=username)

    messages.error(request, 'Action Not Allowed')
    return redirect('panel-user-profile', username=username)


@login_required(login_url='/auth/sign-in')
def panel_user_reset_password(request, username: str) -> HttpResponse:
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

        return redirect('panel-user-profile', username=username)

    messages.error(request, 'Action Not Allowed')
    return redirect('panel-user-profile', username=username)


@login_required(login_url='/auth/sign-in')
def user_view_links(request, username: str) -> HttpResponse:
    context = {

        'page_title': ['Link Control', 'View Links'],
        'request': request,
    }
    user = get_object_or_404(UserAccount, username=username)
    if request.user.username == username or \
            (request.user.account_type == 'moderator' and user.account_type == 'user') or \
            request.user.account_type == 'admin':
        try:
            links = Subscription.objects.filter(assigned_to=user)
            context['links'] = links.filter(is_active=True)
            context['exposed_links'] = links.filter(is_active=True, expose=True)
            context['restricted_links'] = links.filter(is_active=True, expose=False)
        except ObjectDoesNotExist:
            messages.error(request, 'No subscription links were located.')

        return render(request, 'panel/components/page/user-view-links.html', context)

    return error_404(request, username)


@login_required(login_url='/auth/sign-in')
def user_view_single_link(request, shorten_uuid_link) -> HttpResponse:
    context = {
        'page_title': ['Link Control', 'View Links'],
        'request': request,
    }
    try:
        link = Subscription.objects.get(subscription_uuid=shorten_uuid_link)
        if request.user.username == link.assigned_to.username or \
                (request.user.account_type == 'moderator' and link.assigned_to.account_type == 'user') or \
                request.user.account_type == 'admin':
            context['link'] = link
            context['scheme_host'] = request.scheme + '://' + request.get_host()
            if link.expose:
                qrcode_data = generate_qr_code(
                    f'{context.get("scheme_host")}/panel/user/user-link/show/{link.subscription_uuid}'
                )
                context['qrcode'] = qrcode_data

            return render(request, 'panel/components/page/user-view-link-activation.html', context)

    except ObjectDoesNotExist:
        messages.error(request, 'No subscription links were located.')

    return error_404(request, shorten_uuid_link)


@login_required(login_url='/auth/sign-in')
def user_view_single_link_expose(request, shorten_uuid_link) -> HttpResponse:
    try:
        link = Subscription.objects.get(subscription_uuid=shorten_uuid_link)
        if request.user.username == link.assigned_to.username or \
                (request.user.account_type == 'moderator' and link.assigned_to.account_type == 'user') or \
                request.user.account_type == 'admin':
            link.expose = True
            link.save()

            return redirect('user_link_page', shorten_uuid_link=shorten_uuid_link)

    except ObjectDoesNotExist:
        messages.error(request, 'No subscription links were located.')

    return error_404(request, shorten_uuid_link)


@login_required(login_url='/auth/sign-in')
def user_view_single_link_restrict(request, shorten_uuid_link) -> HttpResponse:
    try:
        link = Subscription.objects.get(subscription_uuid=shorten_uuid_link)
        if request.user.username == link.assigned_to.username or \
                (request.user.account_type == 'moderator' and link.assigned_to.account_type == 'user') or \
                request.user.account_type == 'admin':
            link.expose = False
            link.save()

            return redirect('user_link_page', shorten_uuid_link=shorten_uuid_link)

    except ObjectDoesNotExist:
        messages.error(request, 'No subscription links were located.')

    return error_404(request, shorten_uuid_link)


def user_view_single_link_show(request, shorten_uuid_link) -> HttpResponse:
    try:
        link = Subscription.objects.get(subscription_uuid=shorten_uuid_link)

        if link.expose or \
                (request.user.account_type == 'moderator' and link.assigned_to.account_type == 'user') or \
                request.user.account_type == 'admin':
            link.use_count += 1
            link.save()
            return HttpResponse(link_scraper(link.subscription_link))
        else:
            return error_404(request, shorten_uuid_link)

    except ObjectDoesNotExist:
        messages.error(request, 'No subscription links were located.')

    return error_404(request, shorten_uuid_link)
