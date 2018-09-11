from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from common.models import Goods,Types
from datetime import datetime
from common.utils import fileUploadUtil

def index(request):
    '''
    商品信息首页
    :param request:
    :return:
    '''
    goods = Goods.objects.all()
    for good in goods:
        good.typename = Types.objects.get(id=good.typeid).name
    context = {"goodslist":goods}
    return render(request,'console/goods/index.html',context)

def add(request):
    '''
    添加商品信息页面
    :param request:
    :return:
    '''
    typelist = Types.objects.extra(select={"_has":"concat(pid,id)"}).order_by("_has")
    for type in typelist:
        type.pname = "..."*(type.path.count(",")-1)
    context = {"typelist":typelist}
    return render(request,'console/goods/add.html',context)

def insert(request):
    '''
    插入商品信息
    :param request:
    :return:
    '''
    try:
        good = Goods()
        good.picname = fileUploadUtil.picupload(request)
        good.content = request.POST["content"]
        good.goods = request.POST["goods"]
        good.company = request.POST["company"]
        good.price = request.POST["price"]
        good.store = request.POST["store"]
        good.typeid = request.POST["typeid"]
        good.state = 1
        good.addtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        good.save()
    except Exception as err:
        print(err)
    return redirect(reverse("console_good_index"))

def edit(request,gid):
    '''
    商品编辑页面
    :param request:
    :return:
    '''
    typelist = Types.objects.extra(select={"_has": "concat(pid,id)"}).order_by("_has")
    for type in typelist:
        type.pname = "..." * (type.path.count(",") - 1)
    good = Goods.objects.get(id=gid)
    context = {"good":good,"typelist":typelist}
    return render(request,'console/goods/edit.html',context)

def update(request,gid):
    '''
    更新商品信息
    :param request:
    :return:
    '''
    try:
        good = Goods.objects.get(id=gid)
        #判断图片是否修改
        origpicname = good.picname
        postpic = request.POST["picpathname"]
        if origpicname != postpic:
            picname = fileUploadUtil.picupload(request)
            if picname != 0:
                good.picname = picname
                #删除原来服务器上的图片
                if origpicname != "请选择图片":
                    fileUploadUtil.deletepic(origpicname)

        good.goods = request.POST["goods"]
        good.company = request.POST["company"]
        good.content = request.POST["content"]
        good.price = request.POST["price"]
        good.store = request.POST["store"]
        good.typeid = request.POST["typeid"]

        good.save()
    except Exception as err:
        print("更新商品信息异常",err)
    return redirect(reverse('console_good_index'))

def delete(request,gid):
    '''
    删除商品信息
    :param request:
    :return:
    '''
    try:
        good = Goods.objects.get(id=gid)
        picname = good.picname
        good.delete()
        #删除服务器上的图片
        fileUploadUtil.deletepic(picname)
    except Exception as err:
        print("删除商品信息失败：{}",err)
    return redirect(reverse("console_good_index"))
