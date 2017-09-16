from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.forms import Form
from django.forms import fields
from django.forms import widgets
from userlogin import models
import json
# Create your views here.



class UserCheck(Form):  # 注册的form验证
    username = fields.CharField(
        min_length=5,
        max_length=12,
        error_messages={'required': '用户名不能为空',
                        'min_length': '用户名长度不能小于5',
                        'max_length': '用户名长度不能大于12'},
        widget = widgets.TextInput(attrs={'class':'form-control',
                                          'placeholder':'用户名',
                                          'id':'username'})
    )
    password = fields.CharField(
        min_length=5,
        max_length=12,
        error_messages={'required': '密码不能为空',
                        'min_length': '密码长度不能小于5',
                        'max_length': '用户名长度不能大于12'},
        widget=widgets.PasswordInput(attrs={'class': 'form-control',
                                        'placeholder': '密 码',
                                            'id':'password'})
    )
    email = fields.EmailField(
        error_messages={'required': '邮箱不能为空',
                        'invalid':'邮箱格式不正确'},
        widget=widgets.TextInput(attrs={'class': 'form-control',
                                            'placeholder': '邮 箱',
                                        'id':'email'})
    )
    role_id = fields.ChoiceField(
        choices=[],
        initial=3,
        widget=widgets.Select(attrs={'class': 'form-control'})
    )

    def __init__(self,*args,**kwargs):
        super(UserCheck, self).__init__(*args,**kwargs)
        self.fields['role_id'].choices = list(models.Role.objects.values_list('id','role_name'))


class LoginCheck(Form):   # 登陆时的form表单验证
    username = fields.CharField(
        error_messages={'required':'用户名不能为空'},
        widget=widgets.TextInput(attrs={'class': 'form-control',
                                        'placeholder': '用户名'})
    )
    password = fields.CharField(
        error_messages={'required':'密码不能为空'},
        widget = widgets.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': '密 码'})
    )


class UserLogin(View):

    # 定义返回数据字典
    ret_code = {'status':True,'error_msg':{}}

    def get(self, request):
        lc = LoginCheck()
        return render(request, 'login.html',{'data':lc})

    def post(self,request):
        lc = LoginCheck(data=request.POST)
        if lc.is_valid():
            user = lc.cleaned_data['username']
            pwd = lc.cleaned_data['password']
            user_obj = models.User.objects.filter(username=user, password=pwd)
            if not user_obj:
                self.ret_code['status'] = False
                self.ret_code['error_msg'] = {}     # 初始化错误信息
                self.ret_code['error_msg']['username'] = '用户名或密码不正确！'
            else:
                request.session['username'] = user
        else:
            self.ret_code['status'] = False
            self.ret_code['error_msg'] = lc.errors    # 返回错误信息

        return HttpResponse(json.dumps(self.ret_code))


class Register(View):

    # 定义返回数据的字典
    ret_code = {'status':True,'error_msg':{}}

    def get(self,request):
        uc = UserCheck()  # get请求下 返回给页面的Form对象，用于生成Form表单

        return render(request,'register.html',{'data':uc})

    def post(self,request):
        uc = UserCheck(data=request.POST)   # 对用户提交的数据进行验证
        if uc.is_valid():   # 格式通过验证
            username = uc.cleaned_data['username']
            user_obj = models.User.objects.filter(username=username)   # 获取用户输入的用户名，检查是否重复
            if user_obj:  # 存在同名用户，返回错误信息
                self.ret_code['status'] = False
                self.ret_code['error_msg'] = {}
                self.ret_code['error_msg']['username'] = '用户名已存在！'
            else:   # 不存在，新增
                models.User.objects.create(**uc.cleaned_data)
        else:  # 格式不正确，定义错误返回信息
            self.ret_code['status'] = False
            self.ret_code['error_msg'] = {}
            self.ret_code['error_msg'] = uc.errors  # Form表单验证错误信息

        return HttpResponse(json.dumps(self.ret_code))    # 把生成的包含错误信息的字典返回给前端