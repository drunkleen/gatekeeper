from django.contrib import admin
from django.urls import path, include

from core import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/sign-in', views.user_sign_in, name='sign-in'),
    path('auth/sign-up', views.user_sign_up, name='sign-up'),
    path('auth/logout', views.user_sign_out, name='sign-out'),

    path('panel/admin/', views.panel_admin, name='panel-admin'),
    path('panel/admin/user-list', views.panel_admin_user_list, name='panel-admin-user-lists'),
    path('panel/admin/edit-user/<str:username>', views.panel_admin_edit_user, name='admin-edit-user'),
    path('panel/admin/delete-user/<str:username>', views.panel_admin_delete_user, name='admin-delete-user'),

    path('panel/user/<str:username>', views.panel_user_profile_overview, name='panel-user'),
    path('panel/user/profile/<str:username>', views.panel_user_profile_overview, name='panel-user-profile'),
    path('panel/user/edit/<str:username>', views.panel_user_edit, name='edit-user'),
    path('panel/user/reset-password/<str:username>', views.panel_user_reset_password, name='user-reset-password'),


]
