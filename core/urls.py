from django.urls import path

from core import views

urlpatterns = [

    path('', views.index, name='index'),
    path('auth/sign-in', views.user_sign_in, name='sign-in'),
    path('auth/sign-up', views.user_sign_up, name='sign-up'),
    path('auth/logout', views.user_sign_out, name='sign-out'),

    path('auth/forget-password/', views.user_forget_password, name='forget-password'),
    path('auth/reset-password/<str:reset_key>', views.user_reset_password, name='reset-password'),

    path('panel/admin/', views.panel_admin, name='panel-admin'),
    path('panel/admin/user-list', views.panel_admin_user_list, name='panel-admin-user-lists'),
    path('panel/admin/edit-user/<str:username>', views.panel_admin_edit_user, name='admin-edit-user'),
    path('panel/admin/delete-user/<str:username>', views.panel_admin_delete_user, name='admin-delete-user'),

    path(
        'panel/admin/panel-connection',
        views.panel_admin_setting_panel_connection,
        name='panel-admin-setting-panel-connection'
    ),
    path(
        'panel/admin/panel-connection-edit/<int:connection_id>',
        views.panel_admin_setting_panel_edit_connection,
        name='panel-admin-setting-panel-edit-connection'
    ),
    path(
        'panel/admin/panel-connection/<int:connection_id>',
         views.panel_admin_setting_panel_deleted_connection,
         name='panel-admin-setting-panel-deleted-connection'
    ),

    path('panel/admin/create-link/<str:username>', views.panel_admin_create_link, name='admin-create-link'),
    path('panel/admin/edit-link/<str:shorten_uuid_link>', views.panel_admin_edit_link, name='admin-edit-link'),
    path('panel/admin/delete-link/<str:shorten_uuid_link>', views.panel_admin_delete_link, name='admin-delete-link'),

    path('panel/user/<str:username>', views.panel_user_profile_overview, name='panel-user'),
    path('panel/user/profile/<str:username>', views.panel_user_profile_overview, name='panel-user-profile'),
    path('panel/user/edit/<str:username>', views.panel_user_edit, name='edit-user'),
    path('panel/user/panel_user_change_email/<str:username>',
         views.panel_user_change_email, name='user-change-email'),
    path('panel/user/panel_user_reset_password/<str:username>',
         views.panel_user_reset_password, name='user-reset-password'),

    path('panel/user/link/<str:username>', views.user_view_links, name='user-view-links'),

    path('panel/user/user-link/<str:shorten_uuid_link>', views.user_view_single_link, name='user_link_page'),

    path('panel/user/user-link/expose/<str:shorten_uuid_link>',
         views.user_view_single_link_expose, name='user_link_page_expose'),

    path('panel/user/user-link/restrict/<str:shorten_uuid_link>',
         views.user_view_single_link_restrict, name='user_link_page_restrict'),

    path('panel/user/user-link/show/<str:shorten_uuid_link>',
         views.user_view_single_link_show, name='user_link_page_show'),

]