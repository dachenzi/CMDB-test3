from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from userlogin.models import User, Role
from hostmanager.models import Business, Host
from django.utils.decorators import method_decorator
from django.forms import Form
from django.forms import fields
from django.forms import widgets
import json
from userlogin.views import UserCheck


def auth(func):
    def inner(request, *args, **kwargs):
        if request.session.get('username'):
            return func(request, *args, **kwargs)
        else:
            return redirect('/user/login/')

    return inner


class Index(View):
    @method_decorator(auth)
    def get(self, request):
        user_list = User.objects.all()
        host_list = Host.objects.all()
        role_list = Role.objects.all()
        business_list = Business.objects.all()

        return render(request, 'index.html', locals())

class Manager(View):
    @method_decorator(auth)
    def get(self, request):
        host_list = Host.objects.all()
        return render(request, 'manage.html', locals())

    @method_decorator(auth)
    def post(self,request):

        hid = request.POST.get('id',None)

        if hid:

            hostinfo = list(Host.objects.filter(id=hid).values('id','hostname','ip','port','business_id'))
            businfo = list(Business.objects.values_list('id','title'))
            hostinfo[0]['business_list'] = businfo

            return HttpResponse(json.dumps(list(hostinfo)))
        else:
            pass




class HostAdd(Form):
    hostname = fields.CharField(
        max_length=16,
        error_messages={'required': '主机名不能为空',
                        'max_length': '主机名不能超过16位'},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'id': 'hostname', 'placeholder': "主机名",
                                        })
    )
    ip = fields.GenericIPAddressField(
        protocol='ipv4',
        error_messages={'required': 'IP地址不能为空',
                        'invalid': '地址格式不正确'},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'id': 'ip', 'placeholder': " 0.0.0.0",
                                        })
    )
    port = fields.IntegerField(
        max_value=65535,
        error_messages={'required': '端口不能为空',
                        'invalid': '端口范围错误'},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'id': 'port', 'placeholder': " 0",
                                        })
    )
    business_id = fields.ChoiceField(
        choices=[],
        widget=widgets.Select(attrs={'class': 'form-control', 'id': 'business_id'})
    )

    def __init__(self, *args, **kwargs):
        super(HostAdd, self).__init__(*args, **kwargs)
        self.fields['business_id'].choices = Business.objects.values_list('id', 'title')


class AddHost(View):
    ret_code = {'status': True, 'err_msg': {}}

    @method_decorator(auth)
    def get(self, request):
        ha = HostAdd()
        return render(request, 'addhost.html', locals())

    @method_decorator(auth)
    def post(self, request):
        ha = HostAdd(request.POST)
        if ha.is_valid():
            hostobj = Host.objects.filter(ip=ha.cleaned_data['ip'])  # 检查新添加的主机是否重复
            if hostobj:
                self.ret_code['status'] = False
                self.ret_code['err_msg'] = {}
                self.ret_code['err_msg'] = {'ip': 'IP地址已存在!'}
            else:
                self.ret_code['status'] = True
                Host.objects.create(**ha.cleaned_data)
        else:
            self.ret_code['status'] = False
            self.ret_code['err_msg'] = {}
            self.ret_code['err_msg'] = ha.errors

        return HttpResponse(json.dumps(self.ret_code))

class DelHost(View):
    @method_decorator(auth)
    def post(self,request):

        hid = request.POST.get('hid')

        Host.objects.filter(id=hid).delete()

        return HttpResponse(json.dumps('ok'))

class ModifyHost(View):
    @method_decorator(auth)
    def post(self,request):

        hid = request.POST.get('id')
        hostname = request.POST.get('hostname')
        ip = request.POST.get('ip')
        port = request.POST.get('port')
        busname = request.POST.get('business_id')
        businessobj = Business.objects.filter(title=busname).first()

        Host.objects.filter(id=hid).update(hostname=hostname,ip=ip,port=port,business=businessobj)

        return  HttpResponse(json.dumps('ok'))


class BusinessManager(View):
    @method_decorator(auth)
    def get(self, request):
        business_list = Business.objects.all()

        return render(request, 'business.html', locals())


class BusinessAdd(Form):
    title = fields.CharField(
        max_length=16,
        error_messages={'required': '业务线名称不能为空',
                        'max_length': '业务线名称不能超过16'},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'id': 'title', 'placeholder': "名称"})
    )


class AddBusiness(View):
    ret_code = {'status': True, 'err_msg': {}}

    @method_decorator(auth)
    def get(self, request):

        ba = BusinessAdd()

        return render(request, 'addbusiness.html', locals())

    @method_decorator(auth)
    def post(self, request):

        print(request.POST)
        ba = BusinessAdd(data=request.POST)

        if ba.is_valid():

            bus_obj = Business.objects.filter(title=ba.cleaned_data['title'])

            if bus_obj:

                self.ret_code['status'] = False
                self.ret_code['err_msg'] = {'title': '业务线名称已存在！'}

            else:

                self.ret_code['status'] = True
                Business.objects.create(**ba.cleaned_data)

        else:
            self.ret_code['status'] = False
            self.ret_code['err_msg'] = ba.errors

        return HttpResponse(json.dumps(self.ret_code))


class UserInfo(View):
    def get(self, request):
        user_list = User.objects.all()

        return render(request, 'userlist.html', locals())


# class UserAdd(Form):
#     username = fields.CharField(
#         max_length=8,
#         error_messages={'required': '用户名不能为空', 'max_length': '长度不能超过8个字符'},
#         widget = widgets.TextInput(attrs={'class': 'form-control', 'id': 'username', 'placeholder': "用户名"})
#     )
#     password = fields.CharField(
#         max_length=8,
#         error_messages={'required':'密码不能为空','max_length':'长度不能超过8个字符'},
#         widget= widgets.PasswordInput(attrs={'class': 'form-control', 'id': 'username', 'placeholder': "密码"})
#     )


class AddUser(View):

    # 定义返回数据的字典
    ret_code = {'status':True,'error_msg':{}}

    @method_decorator(auth)
    def get(self, request):

        au = UserCheck()

        return render(request,'adduser.html',locals())

    @method_decorator(auth)
    def post(self,request):
        au = UserCheck(data=request.POST)   # 对用户提交的数据进行验证
        if au.is_valid():   # 格式通过验证
            username = au.cleaned_data['username']
            user_obj = User.objects.filter(username=username)   # 获取用户输入的用户名，检查是否重复
            if user_obj:  # 存在同名用户，返回错误信息
                self.ret_code['status'] = False
                self.ret_code['error_msg'] = {}
                self.ret_code['error_msg']['username'] = '用户名已存在！'
            else:   # 不存在，新增
                User.objects.create(**au.cleaned_data)
        else:  # 格式不正确，定义错误返回信息
            self.ret_code['status'] = False
            self.ret_code['error_msg'] = {}
            self.ret_code['error_msg'] = au.errors  # Form表单验证错误信息

        return HttpResponse(json.dumps(self.ret_code))    # 把生成的包含错误信息的字典返回给前端
























