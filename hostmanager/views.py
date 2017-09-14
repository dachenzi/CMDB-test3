from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from userlogin.models import User,Role
from hostmanager.models import Business,Host
from django.utils.decorators import method_decorator
# Create your views here.


def auth(func):
    def inner(request,*args,**kwargs):
        if request.session.get('username'):
            return func(request,*args,**kwargs)
        else:
            return redirect('/user/login/')
    return inner



@method_decorator(auth,name='get')
class Index(View):


    def get(self,request):

        user_list = User.objects.all()
        host_list = Host.objects.all()
        role_list = Role.objects.all()
        business_list = Business.objects.all()
        username = request.session.get('username')

        return render(request,'index.html',locals())

