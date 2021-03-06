﻿from django import forms
from django.forms import ModelForm, TextInput  
from suit.widgets import NumberInput, AutosizedTextarea, HTML5Input, EnclosedInput, SuitDateWidget, \
SuitTimeWidget, SuitSplitDateTimeWidget, LinkedSelect
from django.contrib.auth.forms import PasswordResetForm
from emailmanage.models import CustomUser,Ship,Cargo
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label="用户名")
    password = forms.CharField(label="密码",widget=forms.PasswordInput)


class CustomPasswordResetForm(PasswordResetForm):
    #实现'邮箱未注册'的提示
    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if not User.objects.filter(email=email):
            raise forms.ValidationError('邮箱未注册')
        return email


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='输入密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='重复密码', 
                                widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'email')
        labels = {
        'username':'用户名',
        'email':'Email',
        }
        help_texts = {
            'username': '',
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('两次输入密码不一致!')
        return cd['password2']

class CustomUserForm(ModelForm):  
	class Meta:  
		model = CustomUser  
		fields = ['name','post','telephone','mobile','fax','skype','qq','company_name']
		labels = {
				'name':'姓名',
				'post':'职务',
				'telephone':'办公电话',
				'mobile':'手机',
				'fax':'传真',
				'skype':'Skype',
				'qq':'QQ',
				'company_name':'公司名称',
				}  

		def __init__(self, *args, **kwargs):
			super(CircuitForm, self).__init__(*args, **kwargs)
			for key in self.fields:
				self.fields[key].required = False


class ShipForm(ModelForm):
    class Meta:
            model = Ship
            fields = '__all__'
            widgets={
                'beam': TextInput(attrs={'class': 'input-mini'}),
                'dwt': NumberInput(attrs={'class': 'input-mini'}),
                # 'built': SuitSplitDateTimeWidget,
            }
            


class CargoForm(ModelForm):
    class Meta:
        model = Cargo
        fields = '__all__'