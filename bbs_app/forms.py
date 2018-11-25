# 自定义forms表单
from django import forms
from .models import UserInfo
from django.forms import widgets
from django.core.exceptions import ValidationError


# 使用form表单实现修改密码功能
class ResetForm(forms.Form):
    username = forms.CharField(
        widget=widgets.TextInput(attrs={'class': 'form-control', 'autocomplete': "off", 'placeholder': "请输入用户名"}),
        label='用户名')
    telephone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': "off", 'placeholder': "请输入电话号"}),
        label='手机号', )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "请输入新的密码"}),
        label='新密码')
    repeat_new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "请再次输入新的密码"}),
        label='确认新密码')

    # 定义局部钩子，验证用户名是否已经被注册
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 8:
            raise ValidationError('用户名必须不小于8位（您现在的是{}位）!'.format(len(username)))
        else:
            ret = UserInfo.objects.filter(username=username)
            if not ret:
                raise ValidationError('该用户名还没有被注册!')
            return username

    # 定义局部钩子，验证手机号是否已存在
    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if len(telephone) != 11:
            raise ValidationError('手机号必须是11位的（您现在是{}位）!'.format(len(telephone)))
        else:
            username = self.cleaned_data.get('username')
            ret = UserInfo.objects.filter(username=username, telephone=telephone)
            if ret:
                return telephone
            else:
                raise ValidationError('该用户名对应的手机号不存在!')

    # 定义局部钩子，验证密码位数
    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if len(new_password) < 8:
            raise ValidationError('密码必须不小于8位（您现在的是{}位）!'.format(len(new_password)))
        else:
            return new_password

    # 定义局部钩子，验证确认密码位数
    def clean_repeat_new_password(self):
        repeat_new_password = self.cleaned_data.get('repeat_new_password')
        if len(repeat_new_password) < 8:
            raise ValidationError('密码必须不小于8位（您现在的是{}位）!'.format(len(repeat_new_password)))
        else:
            return repeat_new_password

    # 定义全局钩子，验证两次密码是否相同
    def clean(self):
        if self.cleaned_data.get('new_password') == self.cleaned_data.get('repeat_new_password'):
            return self.cleaned_data
        else:
            raise ValidationError('两次输入的密码不一致!')


# 使用form表单实现注册功能
class RegisterForm(forms.Form):
    username = forms.CharField(
        widget=widgets.TextInput(attrs={'class': 'form-control', 'autocomplete': "off", 'placeholder': "请输入用户名"}),
        label='用户名', error_messages={"required": "用户名必填"})
    telephone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': "off", 'placeholder': "请输入电话号"}),
        label='手机号', error_messages={"required": "手机号必填"})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "请输入密码"}),
                               label='密码', error_messages={"required": "密码必填"})
    repeat_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "请再次输入密码"}),
        label='确认密码', error_messages={"required": "确认密码必填"})
    email = forms.EmailField(widget=widgets.EmailInput(attrs={'class': 'form-control', 'placeholder': "请输入邮箱"}),
                             label='邮箱', error_messages={"required": "邮箱必填"})

    # 定义局部钩子，验证用户名是否已经被注册
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 8:
            raise ValidationError('用户名必须不小于8位（您现在的是{}位）!'.format(len(username)))
        else:
            ret = UserInfo.objects.filter(username=username)
            if ret:
                raise ValidationError('该用户名已经被注册!')
            else:
                return username

    # 定义局部钩子，验证手机号是否已存在
    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if len(telephone) != 11:
            raise ValidationError('手机号必须是11位的（您现在是{}位）!'.format(len(telephone)))
        else:
            ret = UserInfo.objects.filter(telephone=telephone)
            if ret:
                raise ValidationError('该手机号已存在!')
            else:
                return telephone

    # 定义局部钩子，验证密码位数
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError('密码必须不小于8位（您现在的是{}位）!'.format(len(password)))
        else:
            return password

    # 定义局部钩子，验证确认密码位数
    def clean_repeat_password(self):
        repeat_password = self.cleaned_data.get('repeat_password')
        if len(repeat_password) < 8:
            raise ValidationError('密码必须不小于8位（您现在的是{}位）!'.format(len(repeat_password)))
        else:
            return repeat_password

    # 定义全局钩子，验证两次密码是否相同
    def clean(self):
        if self.cleaned_data.get('password') == self.cleaned_data.get('repeat_password'):
            return self.cleaned_data
        else:
            raise ValidationError('两次输入的密码不一致!')