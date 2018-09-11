"""djangoMall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from console.views import index,users,type,goods


urlpatterns = [
    url(r'^$', index.index,name="console_index"),

    #会员管理
    url(r'^users$', users.userindex,name="console_user_index"),
    url(r'^add$', users.useradd,name="console_user_add"),
    url(r'^insert$', users.userinsert,name="console_user_insert"),
    url(r'^edit/(?P<uid>[0-9]+)$', users.useredit,name="console_user_edit"),
    url(r'^update/(?P<uid>[0-9]+)', users.userupdate,name="console_user_update"),
    url(r'^del/(?P<uid>[0-9]+)$', users.userdel,name="console_user_del"),
    url(r'^query/(?P<pagenum>[0-9]+)/(?P<pagesize>[0-9]+)/(?P<keyword>\s*|.*)$', users.query,name="console_user_query"),

    #后台登录
    url(r'^login$', index.login, name="console_login_index"),
    url(r'^dologin$', index.dologin, name="console_login_do"),
    url(r'^verify$', index.verify, name="console_login_verify"),
    url(r'^loginout$', index.loginout, name="console_login_out"),

    #商品类型管理
    url(r'^type$', type.index, name="console_type_index"),
    url(r'^type/add/(?P<tid>[0-9]+)$', type.add, name="console_type_add"),
    url(r'^type/insert$', type.insert, name="console_type_insert"),
    url(r'^type/edit/(?P<tid>[0-9]+)$', type.edit, name="console_type_edit"),
    url(r'^type/update/(?P<tid>[0-9]+)$', type.update, name="console_type_update"),
    url(r'^type/del/(?P<tid>[0-9]+)$', type.delete, name="console_type_del"),

    #商品管理
    url(r'^goods$',goods.index,name="console_good_index"),
    url(r'^goods/add$',goods.add,name="console_good_add"),
    url(r'^goods/insert$',goods.insert,name="console_good_insert"),
    url(r'^goods/edit/(?P<gid>[0-9]+)$',goods.edit,name="console_good_edit"),
    url(r'^goods/update/(?P<gid>[0-9]+)$',goods.update,name="console_good_update"),
    url(r'^goods/del/(?P<gid>[0-9]+)$',goods.delete,name="console_good_del"),
]
