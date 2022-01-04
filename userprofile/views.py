from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from .forms import UserLoginForm


# Create your views here.

def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # .cleaned_data 清洗出合法数据
            data = user_login_form.cleaned_data
            # 检验账号、密码是否正确匹配数据库中的某个用户
            # 如果均匹配则返回这个 user 对象
            user = authenticate(username=data['username'], password=data['password'])
            # is_authenticated是models.User类的属性，用于判断用户是否已通过身份验证
            # 用在{% if user.is_authenticated %}
            if user:
                # 将用户数据保存在 session 中，即实现了登录动作
                login(request, user)
                return redirect("articlesapp:articles")
            else:
                return HttpResponse("账号或密码输入有误❎")
                # return redirect('userprofile:login')
        else:
            return HttpResponse("账号或密码输入不合法")
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form': user_login_form}
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")

# 用户退出
def user_logout(request):
    logout(request)
    return redirect("articlesapp:articles")

# 跟发表文章的表单类类似，Form对象的主要任务就是验证数据。调用is_valid()方法验证并返回指定数据是否有效的布尔值。

# Form不仅负责验证数据，还可以“清洗”它：将其标准化为一致的格式，这个特性使得它允许以各种方式输入特定字段的数据，并且始终产生一致的输出。一旦Form使用数据创建了一个实例并对其进行了验证，就可以通过cleaned_data属性访问清洗之后的数据。
#
# authenticate()方法验证用户名称和密码是否匹配，如果是，则将这个用户数据返回。
#
# login()方法实现用户登录，将用户数据保存在session中。