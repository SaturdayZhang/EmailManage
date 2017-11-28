﻿from django.conf.urls import url
from django.contrib.auth.views import login,logout,logout_then_login,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register/complete/$', views.register_complete, name='users_registration_complete'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',  views. activate, name='users_activate'),
    url(r'^activate/complete/$', views.activation_complete, name='users_activation_complete'),
    #url(r'^password_reset_email/$', views.password_reset_email, name='password_reset_email'),
    #url(r'^password_reset_form/$', views.password_reset_form, name='password_reset_form'),
    #url(r'^password_reset_done/$', views.password_reset_done, name='password_reset_done'),
    url(r'^login_main/$', views.login_main, name='login_main'),
    url(r'^tonnage/$', views.tonnage, name='tonnage'),
    url(r'^cargo/$', views.cargo, name='cargo'),
    url(r'^tct/$', views.tct, name='tct'),
    url(r'^port/$', views.port, name='port'),    
    url(r'^agent/$', views.agent, name='agent'),
    url(r'^tonnage_selected/$', views.tonnage_selected, name='tonnage_selected'),
    url(r'^cargo_selected/$', views.cargo_selected, name='cargo_selected'),
    url(r'^tct_selected/$', views.tct_selected, name='tct_selected'),
    url(r'^port_selected/$', views.port_selected, name='port_selected'),    
    url(r'^agent_selected/$', views.agent_selected, name='agent_selected'),
    url(r'^ship_cargo/$', views.ship_cargo, name='ship_cargo'),    
    url(r'^ship_tct/$', views.ship_tct, name='ship_tct'),
    url(r'^logout/$',  logout, name='logout'),
    url(r'^logout-then-login/$',logout_then_login, name='logout_then_login'),
    #url(r'^password_change_form/$', views.password_change_form, name='password_change_form'),
    #url(r'^password_change_done/$', views.password_change_done, name='password_change_done'),
    url(r'^password_change/$', views.CustomPasswordChangeView.as_view(), name='password_change'),
    url(r'^password_change/done/$', views.CustomPasswordChangeDoneView.as_view(), name='password_change_done'),

    url(r'^password_reset/$', views.CustomPasswordResetView.as_view(), name='password_reset'),
    url(r'^password_reset/done/$', PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^reset/done/$', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
