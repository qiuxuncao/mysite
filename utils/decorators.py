from account.views import user_login
from django.shortcuts import redirect


def login_wrapper(view_func):
    '''
    判断登录装饰器
    :param view_func:
    :return:
    '''
    def inner(request):
        if request.session.get('is_login'):
            # print('获取到登陆session啦')
            return view_func(request)
        else:
            print('没有登录session')
            return redirect('/account/login2')
    return inner
