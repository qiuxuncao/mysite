from django.shortcuts import render, redirect
from django.contrib import sessions
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
# Create your views here.


def user_login(request):

    if request.method == 'GET':
        login_form = LoginForm()
        return render(request, "account/login2.html", {"form": login_form})

    if request.method == 'POST':

        #request.POST将前台数据传递给表单类，生成一个绑定实例
        login_form = LoginForm(request.POST)
        #如果数据合法则进行数据清洗，返回输入的数据（字典格式）
        if login_form.is_valid():
            cd = login_form.cleaned_data
            # 如果给定的凭据有效则返回一个User对象，否则返回None
            user = authenticate(username=cd['username'], password=cd['password'])

            if user:
                #如果user不为None(既通过了凭据验证返回了user对象)，使用系统自带的login方法登录
                login(request, user)
            else:
                error_msg = "账号与密码不匹配"
                return render(request, 'account/login2.html', {'form': login_form, 'error_msg': error_msg})
        else:
            error_msg = '请输入合法数据'
            return render(request, 'account/login2.html', {'form': login_form, 'error_msg': error_msg})
        # 校验成功后跳转至blog

        request.session['is_login'] = True
        request.session['username'] = cd['username']
        request.session.set_expiry(100)

        return redirect('/blog/')
