from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse, Http404
from django.contrib import messages
from core.models import UserAccount, Subscription, PanelConnection
from core.forms import UserCreationForm, AdminUserCreationForm, AdminUserEditForm, UserEditForm, \
    UserPasswordChangeForm, UserEmailChangeForm, SubscriptionForm, SubscriptionEditForm, AdminConnectionCreationForm
from core.utils.utils import generate_qr_code, link_scraper
from django.utils import timezone
from datetime import timedelta

from core.utils.link_detail_api_service import get_user_info


# util functions

def is_admin_or_moderator(user):
    return user.account_type in ('admin', 'moderator')


def is_allowed_to_edit(user, target_user):
    return user.account_type == 'admin' or \
        (user.account_type == 'moderator' and target_user.account_type == 'user') or \
        (user.account_type == 'moderator' and target_user.username == user.username) or \
        target_user.username == user.username


def is_allowed_to_delete(user, target_user):
    return user.account_type == 'admin' or \
        (user.account_type == 'moderator' and target_user.account_type == 'user') or \
        (user.account_type == 'moderator' and target_user.username == user.username)


def has_permission(request, user):
    return (
            request.user.account_type == 'admin' or
            (request.user.account_type == 'moderator' and user.account_type == 'user') or
            (request.user.account_type == 'moderator' and user.username == request.user.username) or
            user.username == request.user.username
    )


def redirect_based_on_user_type(user):
    if is_admin_or_moderator(user):
        return redirect('panel-admin')
    else:
        return redirect('panel-user', username=user.username)


def handle_form_errors(request, form):
    for field, errors in form.errors.items():
        for error in errors:
            messages.error(request, f'Error in {field}: {error}')


def get_subscription_links(user):
    try:
        links = Subscription.objects.filter(assigned_to=user)
        return links.filter(is_active=True)
    except ObjectDoesNotExist:
        return None


def handle_object_does_not_exist(request):
    messages.error(request, 'No subscription links were located.')
    raise Http404("No subscription links were located.")


# view methods


def index(request) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect_based_on_user_type(request.user)
    return redirect('sign-in')


def user_sign_in(request) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect_based_on_user_type(request.user)

    user_ip = request.META['REMOTE_ADDR']
    request.session['user_ip'] = user_ip

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
    if is_admin_or_moderator(request.user):
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
    if is_admin_or_moderator(request.user):

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
def panel_admin_delete_link(request, shorten_uuid_link: str) -> HttpResponse:
    if is_admin_or_moderator(request.user):

        link = get_object_or_404(Subscription, subscription_uuid=shorten_uuid_link)

        if is_allowed_to_delete(request.user, link.assigned_to):
            link.delete()
            return redirect('user-view-links', username=link.assigned_to.username)

    raise PermissionDenied


@login_required(login_url='/auth/sign-in')
def panel_admin_delete_user(request, username: str) -> HttpResponse:
    if is_admin_or_moderator(request.user):

        user = UserAccount.objects.get(username=username)

        if is_allowed_to_edit(request.user, user):
            user.delete()
            return redirect('panel-admin-user-lists')

    raise PermissionDenied


@login_required(login_url='/auth/sign-in')
def panel_admin_setting_panel_connection(request) -> HttpResponse:
    if request.user.account_type == 'admin':
        context = {
            'request': request,
            'page_title': ['Panel Setting', 'Panel Connection'],
        }

        if request.method == 'POST':
            form = AdminConnectionCreationForm(request.POST)
            if form.is_valid():
                form.save()

        panel_connections = PanelConnection.objects.all()
        context['panel_connections'] = panel_connections

        context['connection_creation_form'] = AdminConnectionCreationForm()

        return render(request, 'panel/components/page/admin-setting-panel-connection.html', context)

    return redirect('panel-user', username=request.user.username)


@login_required(login_url='/auth/sign-in')
def panel_admin_setting_panel_deleted_connection(request, connection_id: int) -> HttpResponse:
    if request.user.account_type == 'admin':
        panel_connection = get_object_or_404(PanelConnection, id=connection_id)
        panel_connection.delete()
        return redirect('panel-admin-setting-panel-connection')

    raise PermissionDenied


@login_required(login_url='/auth/sign-in')
def panel_user_profile_overview(request, username: str) -> HttpResponse:
    context = {
        'request': request,
    }

    if request.user.username == username or is_admin_or_moderator(request.user):
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
            if has_permission(request, user):
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
            handle_form_errors(request, form)

        return redirect('panel-user-profile', username=username)

    messages.error(request, 'Action Not Allowed')
    return redirect('panel-user-profile', username=username)


@login_required(login_url='/auth/sign-in')
def panel_user_change_email(request, username):
    user = get_object_or_404(UserAccount, username=username)

    if request.method == 'POST':
        form = UserEmailChangeForm(request.POST, instance=user)

        if form.is_valid():
            if request.user.account_type == 'admin' or \
                    (request.user.account_type == 'moderator' and user.account_type == 'user') or \
                    (request.user.account_type == 'moderator' and user.username == request.user.username) or \
                    user.username == request.user.username:
                form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your E-mail was successfully updated!')
        else:
            handle_form_errors(request, form)

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
            handle_form_errors(request, form)

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

    raise Http404("No subscription links were located.")


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

            if link.panel_connection:
                context['link_details'] = get_user_info(link)

            if link.expose:
                qrcode_data = generate_qr_code(
                    f'{context.get("scheme_host")}/panel/user/user-link/show/{link.subscription_uuid}'
                )
                context['qrcode'] = qrcode_data

            return render(request, 'panel/components/page/user-view-link-activation.html', context)

    except ObjectDoesNotExist:
        handle_object_does_not_exist(request)


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
        handle_object_does_not_exist(request)


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
        handle_object_does_not_exist(request)


def user_view_single_link_show(request, shorten_uuid_link) -> HttpResponse:
    user_ip = request.META['REMOTE_ADDR']
    stored_ip = request.session.get('user_ip', None)

    try:

        link = Subscription.objects.get(subscription_uuid=shorten_uuid_link)

        if link.expose or \
                ((stored_ip and user_ip) == stored_ip) or \
                (request.user.account_type == 'moderator' and link.assigned_to.account_type == 'user') or \
                request.user.account_type == 'admin':
            link.use_count += 1
            link.save()
            return HttpResponse(link_scraper(link.subscription_link))
        else:
            raise Http404("No subscription link were located.")

    except ObjectDoesNotExist:
        handle_object_does_not_exist(request)
