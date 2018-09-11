from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render
from common.models import Users
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.db.models import Q


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

        import hashlib
        m = hashlib.md5()
        m.update(bytes(request.POST["password"],encoding='utf8'))
        user.password = m.hexdigest()

        user.save()
    except Exception as err:
        print(err)
    return redirect(reverse('console_user_query'))

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
    except Exception as err:
        print(err)
    return redirect(reverse('console_user_index'))

def userdel(request,uid):
    try:
        user = Users.objects.get(id=uid)
        user.delete()
    except Exception as err:
        print(err)
    return redirect(reverse('console_user_index'))

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
