from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.core.urlresolvers import reverse
from common.models import Types

def index(request):
    '''
    商品类型首页
    :param request:
    :return:
    '''
    typelist = Types.objects.extra(select={'_has':'concat(pid,id)'}).order_by('_has')
    for type in typelist:
        type.pname = "..."*(type.path.count(',')-1)
    context = {"typelist":typelist}
    return render(request,'console/type/index.html',context)

def add(request,tid):
    '''
    添加商品类型页面
    :param request:
    :return:
    '''
    if not tid or tid == '0':
        context = {"pid":'0','path':"0,"}
    else:
        type = Types.objects.get(id=tid)
        context = {'pid':type.id,'path':type.path,'name':type.name}
    return render(request,'console/type/add.html',context)

def insert(request):
    '''
    添加商品类型
    :param request:
    :param tid:
    :return:
    '''
    try:
        type = Types()
        type.name = request.POST['name']
        type.pid = request.POST['pid']
        if type.pid == '0':
            type.path = request.POST["path"]
        else:
            type.path = request.POST["path"] + type.pid + ","
        type.save()
    except Exception as err:
        print(err)
    return redirect(reverse('console_type_index'))

def edit(request,tid):
    '''
    编辑商品类型页面
    :param request:
    :param tid:
    :return:
    '''
    type = Types.objects.get(id=tid)
    context = {'type':type}
    return render(request,'console/type/edit.html',context)

def update(request,tid):
    '''
    更新商品类型页面
    :param request:
    :return:
    '''
    try:
        type = Types.objects.get(id=tid)
        type.name = request.POST['name']
        type.save()
    except Exception as err:
        print(err)
    return redirect(reverse('console_type_index'))

def delete(request,tid):
    '''
    删除商品类别
    :param request:
    :return:
    '''
    try:
        types = Types.objects.filter(pid=tid).count()
        if types > 0:
            context = {"info":"该类别下含有子类别,不能删除"}
            return render(request,'console/info.html',context)
        else:
            type = Types.objects.get(id=tid)
            if type:
                type.delete()
    except Exception as err:
        print(err)
    return redirect(reverse("console_type_index"))