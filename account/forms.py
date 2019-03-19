from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, UserInfo


class LoginForm(forms.Form):
    # 提交表单后对数据不修改,继承Form
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    # 如果要写入或者修改数据则需要继承ModelForm
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        # 声明本表单类所应用的数据模型,数据写入哪个数据库表中
        model = User
        # 将username和email两个属性，插入user表中，上面的password和password2为重新定义的属性字段，会覆盖到user中，所以不需要在内部类Meta中声明
        fields = ('username', 'email')

    #校验两次输入的密码是否一致
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('password do not match')
        return cd['password2']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone','birth')


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ("school", "company","profession","address", "aboutme")


#emai信息来自于User表，也需要表单类
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)