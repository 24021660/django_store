from django import forms


class UserForm(forms.Form):
    username=forms.CharField(label='用户名',max_length=100)
    password=forms.CharField(label='密码',widget=forms.PasswordInput())
    email=forms.EmailField(label='电子邮件')
