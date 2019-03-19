
from django.shortcuts import render, redirect,HttpResponseRedirect
from .forms import LoginForm, RegistrationForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import UserInfo, UserProfile
# from utils.decorators import login_wrapper
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

        # 设置session信息
        request.session['is_login'] = True
        request.session['username'] = cd['username']
        #设置session有效期为？秒，不管操作不操作系统，10秒后都会自动失效
        request.session.set_expiry(10)

        # 校验成功后跳转至blog
        return redirect('/blog/')


def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        if user_form.is_valid() * userprofile_form.is_valid():
            new_user = user_form.save(commit=False)
            #给new_user设置密码
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            UserInfo.objects.create(user=new_user)
            # return HttpResponse('注册成功')
            return HttpResponseRedirect('/account/login2/')
        else:
            return HttpResponse('对不起，注册失败')
    else:
        user_form =RegistrationForm()
        userprofile_form = UserProfileForm()
        return render(request, 'account/register.html', {'form': user_form, 'profile':userprofile_form})


# @login_wrapper
def myself(request):
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=user)
    userinfo = UserInfo.objects.get(user=user)
    return render(request, "account/myself.html", {'user': user, 'userprofile': userprofile, 'userinfo': userinfo})