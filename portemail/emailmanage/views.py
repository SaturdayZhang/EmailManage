from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login,get_user_model
from django.contrib.auth.views import PasswordResetView,PasswordChangeView,PasswordChangeDoneView
from django.contrib.auth.models import User
from django import forms
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.template.response import TemplateResponse

from .forms import LoginForm,UserRegistrationForm,CustomUserForm,CustomPasswordResetForm 
from .models import CustomUser 
from .compat import urlsafe_base64_decode
from .utils import EmailActivationTokenGenerator, send_activation_email
from .signals import user_activated, user_registered
from .conf import settings

import sys

# Create your views here.

def index(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],password=cd['password'])            
            if user is not None:                
                context={'user':user,'has_permission':True}
                if user.is_active:                   
                    login(request, user)
                    #return render(request, 'emailmanage/login_main.html', context)
                    return render(request, 'admin/index.html')
                else:
                    
                    opts = {
                        'user':user,
                        'request': request,
                        'from_email': settings.DEFAULT_FROM_EMAIL,
                        'email_template': 'emailmanage/activation_email.html',
                        'subject_template': 'emailmanage/activation_email_subject.html',
                        'html_email_template': None,
                    }
                    send_activation_email(**opts) 
                    user_registered.send(sender=new_user.__class__, request=request, user=user)
                    return redirect(reverse('users_registration_complete'))                    
            else:
                return HttpResponse('不合法用户')
    else:
        form = LoginForm()
    return render(request, 'emailmanage/index.html', {'form': form})


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        profile_form = CustomUserForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)                
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.is_active=False           
            new_user.save()
            cd = profile_form.cleaned_data
            user_profile =CustomUser.objects.create(user = new_user)
            user_profile.name = cd['name']
            user_profile.post = cd['post']
            user_profile.telephone = cd['telephone']
            user_profile.mobile = cd['mobile']
            user_profile.fax = cd['fax']
            user_profile.skype = cd['skype']
            user_profile.qq = cd['qq']
            user_profile.company_name = cd['company_name']
            user_profile.save() 
            if  settings.USERS_AUTO_LOGIN_AFTER_REGISTRATION:
                new_user.is_active=True          
                new_user.save()
                login(request, new_user)
                return redirect(resolve_url(settings.LOGIN_URL))                
            elif not new_user.is_active and settings.USERS_VERIFY_EMAIL:
                opts = {
                    'user':new_user,
                    'request': request,
                    'from_email': settings.DEFAULT_FROM_EMAIL,
                    'email_template': 'emailmanage/activation_email.html',
                    'subject_template': 'emailmanage/activation_email_subject.html',
                    'html_email_template': None,
                }
                send_activation_email(**opts) 
                user_registered.send(sender=new_user.__class__, request=request, user=new_user)
            return redirect(reverse('users_registration_complete'))
    else:
        user_form = UserRegistrationForm()
        profile_form = CustomUserForm()
    return render(request, 'emailmanage/register.html',{'user_form': user_form,'profile_form': profile_form})


def register_complete(request,
                      template_name='emailmanage/registration_complete.html',
                      current_app=None,
                      extra_context=None):
    context = {
        'login_url': reverse('index'),
        'title': '注册成功',
    }
    if extra_context is not None:  # pragma: no cover
        context.update(extra_context)
    return TemplateResponse(request, template_name, context)
    
def activate(request,
             uidb64=None,
             token=None,
             template_name='emailmanage/activate.html',
             post_activation_redirect=None,
             current_app=None,
             extra_context=None):

    context = {
        'title': _('Account activation '),
    }

    if post_activation_redirect is None:
        post_activation_redirect = reverse('users_activation_complete')

    UserModel = get_user_model()
    assert uidb64 is not None and token is not None

    token_generator = EmailActivationTokenGenerator()

    try:
        uid = urlsafe_base64_decode(uidb64)
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()        
        user_activated.send(sender=user.__class__, request=request, user=user)
        if settings.USERS_AUTO_LOGIN_ON_ACTIVATION:
            login(request, user)
            messages.info(request, '感谢激活，您可以登录')
        return redirect(post_activation_redirect)
    else:
        title = '邮箱确认失败'
        context = {
            'title': title,
        }

    if extra_context is not None:  # pragma: no cover
        context.update(extra_context)
    return TemplateResponse(request, template_name, context)

def activation_complete(request,
                        template_name='emailmanage/activation_complete.html',
                        current_app=None,
                        extra_context=None):
    context = {
        'title': '账户激活完成',
    }
    if extra_context is not None:  # pragma: no cover
        context.update(extra_context)
    return TemplateResponse(request, template_name, context)



   
def password_reset_email(request):
    return render(request, 'emailmanage/password_reset_email.html')
    
    
def password_reset_form(request):
    return render(request, 'emailmanage/password_reset_form.html')


def password_reset_done(request):
    return render(request, 'emailmanage/password_reset_done.html')




class CustomPasswordResetView(PasswordResetView):
    template_name = 'emailmanage/password_reset_form.html'
    form_class = CustomPasswordResetForm 


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'emailmanage/password_change_form.html'


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'emailmanage/password_change_done.html'


def login_main(request):
    return render(request, 'emailmanage/login_main.html')
    
    
def tonnage(request):
    context = {
        'selected': '/tonnage/',
        'title':  'tonnage 信息',
    }
    return render(request, 'emailmanage/tonnage.html',context)
    
def cargo(request):
    context = {
    		'selected': '/cargo/',
        'title':  'cargo 信息',
    }
    return render(request, 'emailmanage/cargo.html',context)
    
    
def tct(request):
    context = {
    		'selected': '/tct/',
        'title':  'tct信息',
    }
    return render(request, 'emailmanage/tct.html',context)
    
    
def port(request):
    context = {
    		'selected': '/port/',
        'title':  'port 信息',
    }
    return render(request, 'emailmanage/port.html',context)
    
def agent(request):
    context = {
    		'selected': '/agent/',
        'title': 'agent 信息',
    }
    return render(request, 'emailmanage/agent.html',context)
    
    
def tonnage_selected(request):
    context = {
    		'selected': '/tonnage_selected/',
        'title':  'tonnage 筛选信息',
    }
    return render(request, 'emailmanage/tonnage_selected.html',context)
    
def cargo_selected(request):
    context = {
        'selected': '/cargo_selected/',
        'title': 'cargo 筛选信息',
    }
    return render(request, 'emailmanage/cargo_selected.html',context)
    
    
def tct_selected(request):
    context = {
    		'selected': '/tct_selected/',
        'title':  'tct筛选信息',
    }
    return render(request, 'emailmanage/tct_selected.html',context)
    
    
def port_selected(request):
    context = {
    		'selected': '/port_selected/',
        'title':  'port 筛选信息',
    }
    return render(request, 'emailmanage/port_selected.html',context)
    
def agent_selected(request):
    context = {
    		'selected': '/agent_selected/',
        'title': 'agent 筛选信息',
    }
    return render(request, 'emailmanage/agent_selected.html',context)

    
    
def ship_cargo(request):
    context = {
    		'selected': '/ship_cargo/',
        'title':  'Tonnage和cargo 匹配信息',
    }
    return render(request, 'emailmanage/ship_cargo.html',context)
    
def ship_tct(request):
    context = {
    		'selected': '/ship_tct/',
        'title':  'Tonnage和tct 匹配信息',
    }
    return render(request, 'emailmanage/ship_tct.html',context)
    
    
def logout(request):
    # clear cookie and session
    return render(request, 'emailmanage/index.html')
    
    
def password_change_form(request):
    return render(request, 'emailmanage/password_change_form.html')
    
    
def password_change_done(request):
    return render(request, 'emailmanage/password_change_done.html')
