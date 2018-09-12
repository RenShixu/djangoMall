from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render
from common.models import Users
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.db.models import Q
from common.utils import encryptionUtil


def userindex(request):
    users = Users.objects.all()
    context = {"users":users}
    return render(request,'console/users/index.html',context)

def useradd(request):
    return render(request,'console/users/add.html')

def userinsert(request):
    try:
        user = Users()
        user.name = request.POST["name"]
        user.username = request.POST['username']
        user.email = request.POST["email"]
        user.addtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user.sex = request.POST["sex"]
        user.phone = request.POST["phone"]
        user.code = request.POST["code"]
        user.address = request.POST["address"]
        user.state = 1
        user.password = encryptionUtil.getencodepassword(request.POST["password"])
        user.save()
        context = {"info":"添加用户信息成功"}
    except Exception as err:
        context = {"info": "添加用户信息失败"}
        print(err)
    return render(request, "console/users/edit.html", context)

def useredit(request,uid):
    user = Users.objects.get(id=uid)
    context = {"user":user}
    return render(request,"console/users/edit.html",context)

def userupdate(request,uid):
    try:
        user = Users.objects.get(id=uid)

        user.name = request.POST["name"]
        user.sex = request.POST["sex"]
        user.address = request.POST["address"]
        user.code = request.POST["code"]
        user.phone = request.POST["phone"]
        user.email = request.POST["email"]
        user.state = request.POST["state"]

        user.save()
        context = {"info": "用户信息更新成功"}
    except Exception as err:
        context = {"info": "用户信息更新失败"}
        print(err)
    return render(request, 'console/info.html', context)

def userdel(request,uid):
    try:
        user = Users.objects.get(id=uid)
        user.delete()
        context = {"info": "删除成功"}
    except Exception as err:
        context = {"info": "删除失败"}
        print(err)
    return render(request,'console/info.html',context)

def query(request,pagenum,pagesize,keyword):
    '''
    会员信息查询
    :param request:
    :return:
    '''
    ky = ""
    if str(request.method) == "GET":
        ky = keyword
    else:
        ky = request.POST["keyword"]

    if not pagenum:
        pagenum = 1
    if not pagesize:
        pagesize = 3
    users = Users.objects.filter(Q(username__icontains=ky) | Q(name__icontains=ky))
    pageLists = Paginator(users,int(pagesize))
    currentpagelist = pageLists.page(int(pagenum))
    pagerange = pageLists.page_range
    maxpagenum = max(pagerange)
    nextpage = int(pagenum)+1
    prepage = int(pagenum)-1
    if prepage == 0:
        prepage = 1
    if pagenum == maxpagenum:
        nextpage = maxpagenum

    context = {"users":currentpagelist,"pagerange":pagerange,
               "pagenum":str(pagenum),"keyword":ky,"maxpagenum":str(maxpagenum),
               "nextpage":str(nextpage),"prepage":str(prepage)}
    return render(request,"console/users/index.html",context)

def resetpassword(request,uid):
    '''
    重置密码页面
    :param request:
    :param uid:
    :return:
    '''
    context = {"uid":uid}
    return render(request,'console/users/resetcode.html',context)

def modifypassword(request):
    '''
    修改密码
    :param request:
    :return:
    '''
    password = request.POST["password"]
    repassword = request.POST["repassword"]
    if password != repassword:
        context = {"info":"两次输入的密码不一致"}
        return render(request,'console/info.html',context)

    try:
        user = Users.objects.get(id=request.POST["uid"])
        encodepassword = encryptionUtil.getencodepassword(password)

        if encodepassword != user.password:
            user.password = encodepassword
            user.save()
    except Exception as err:
        print(err)
    context = {"info":"密码修改成功"}
    return render(request,"console/info.html",context)