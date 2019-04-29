import logging
from django import forms
from django.forms import ModelForm
from django.contrib.auth import hashers

from login.models import *


class LoginModel(ModelForm):
    rememberMe = forms.BooleanField(label='记住我', required=False)

    class Meta:
        model = Player
        fields = ['playerMail', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'placehold': '请输入你的密码...'}),
            'playerMail': forms.TextInput(attrs={'placehold': '请输入你的邮箱...'}),
        }
        labels = {
            'playerMail': '邮箱',
            'password': '密码'
        }

    def clean(self):
        cleanedData = super(LoginModel, self).clean()
        cPlayerMail = cleanedData.get("playerMail")
        try:
            player = Player.objects.get(playerMail__iexact=cPlayerMail)
            if hashers.check_password(cleanedData.get("password"), player.password):
                logging.debug(cleanedData.get("rememberMe"))
            else:
                raise forms.ValidationError("邮箱或密码错误")
        except Player.DoesNotExist:
            raise forms.ValidationError("邮箱或密码错误")


class RefisterForm(ModelForm):
    confirm = forms.CharField(label='确认密码', widget=forms.PasswordInput(attrs={'placehoder': '再次输入你的密码...'}))

    class Meta:
        model = Player
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': '输入你的密码...'}),
            'playerName': forms.TextInput(attrs={'placeholder': '请输入你的用户名...'}),
            'playerPhone': forms.TextInput(attrs={'placeholder': '请输入你的电话...'}),
            'playerMail': forms.TextInput(attrs={'placeholder': '请输入你的邮箱...'}),
        }
        labels = {
            'playerMail': '邮箱',
            'playerName': '用户名',
            'playerPhone': '电话',
            'password': '密码',
        }

    def clean(self):
        cleanedData =super(RefisterForm, self).clean()
        password = cleanedData.get("password")
        confirm = cleanedData.get("confirm")
        logging.debug("Cleaned")
        if password != confirm:
            raise forms.ValidationError("你的密码不一致")
        if Player.objects.filter(playerMail__iexact=cleanedData.get("playerMail")).exists():
            raise forms.ValidationError("邮箱已被注册")
        if Player.objects.filter(playerName__iexact=cleanedData.get("playerName")).exists():
            raise forms.ValidationError("用户名已被占用")
