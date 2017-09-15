from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from userlogin.models import User, Role
from hostmanager.models import Business, Host
from django.utils.decorators import method_decorator
from django.forms import Form
from django.forms import fields
from django.forms import widgets
import json

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
        error_messages={'required':'端口不能为空',
                        'invalid':'端口范围错误'},
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

    ret_code ={'status':True,'err_msg':{}}

    @method_decorator(auth)
    def get(self, request):
        ha = HostAdd()
        return render(request, 'addhost.html', locals())

    @method_decorator(auth)
    def post(self,request):
        ha = HostAdd(request.POST)
        if ha.is_valid():
            hostobj = Host.objects.filter(ip=ha.cleaned_data['ip'])   # 检查新添加的主机是否重复
            if hostobj:
                self.ret_code['status'] = False
                self.ret_code['err_msg'] = {}
                self.ret_code['err_msg'] = {'ip':'IP地址已存在!'}
            else:
                self.ret_code['status'] = True
                Host.objects.create(**ha.cleaned_data)
        else:
            self.ret_code['status'] = False
            self.ret_code['err_msg'] = {}
            self.ret_code['err_msg'] = ha.errors

        return HttpResponse(json.dumps(self.ret_code))



class BusinessManager(View):

    @method_decorator(auth)
    def get(self,request):

        business_list = Business.objects.all()

        return render(request,'business.html',locals())



class BusinessAdd(Form):

    title = fields.CharField(
        max_length=16,
        error_messages={'required':'业务线名称不能为空',
                        'max_length':'业务线名称不能超过16'},
        widget = widgets.TextInput(attrs={'class': 'form-control', 'id': 'title', 'placeholder': "名称"})
    )


class AddBusiness(View):

    ret_code = {'status':True,'err_msg':{}}

    @method_decorator(auth)
    def get(self, request):

        ba = BusinessAdd()

        return render(request,'addbusiness.html',locals())

    def post(self,request):

        print(request.POST)
        ba = BusinessAdd(data=request.POST)

        if ba.is_valid():

            bus_obj = Business.objects.filter(title=ba.cleaned_data['title'])

            if bus_obj:

                self.ret_code['status'] = False
                self.ret_code['err_msg'] = {'title':'业务线名称已存在！'}

            else:

                self.ret_code['status'] = True
                Business.objects.create(**ba.cleaned_data)

        else:
            self.ret_code['status'] = False
            self.ret_code['err_msg'] = ba.errors

        return HttpResponse(json.dumps(self.ret_code))


class UserInfo(View):

    def get(self,request):

        user_list = User.objects.all()

        return render(request,'userlist.html',locals())