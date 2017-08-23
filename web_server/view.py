# *_*coding:utf-8 *_*
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# python D:/python_workplace/pc-status-supervision/web_server/manage.py runserver 0.0.0.0:8000
import data


# 返回ok表示代理服务器在线
def hello(request):
    return HttpResponse("ok")


# 接收PC的GET传值并进行数据更新，数据存在data.py中,目前并未采用该方式
def update(request):
    if request.method == 'GET':
        msg = request.GET.get('msg', 'get no data')
        name = request.GET.get('name', 'get no data')
        if name == 'port':
            data.port = msg
        elif name == 'cdrom_exist':
            data.cdrom_exist = msg
        elif name == 'cdrom_state':
            data.cdrom_state = msg
        elif name == 'sysinfo':
            data.sysinfo = msg
        elif name == 'user':
            data.user = msg
        elif name == 'usb':
            data.usb = msg
        elif name == 'ip':
            data.ip = msg
        elif name == 'serial':
            data.serial = msg
        elif name == 'parallel':
            data.parallel = msg
        return HttpResponse(msg)


# 相应来自前端的get请求
def query(request):
    if request.method == 'GET':
        name = request.GET.get('name', 'get no data')
        if name == 'port':
            msg = data.port
        elif name == 'cdrom_exist':
            msg = data.cdrom_exist
        elif name == 'cdrom_state':
            msg = data.cdrom_state
        elif name == 'sysinfo':
            msg = data.sysinfo
        elif name == 'user':
            msg = data.user
        elif name == 'usb':
            msg = data.usb
        elif name == 'ip':
            msg = data.ip
        elif name == 'serial':
            msg = data.serial
        elif name == 'parallel':
            msg = data.parallel
        elif name == 'query_all':
            msg = data.query_all()
        elif name == 'query_bytime':
            sdate = request.GET.get('sdate', 'get no data')
            edate = request.GET.get('edate', 'get no data')
            msg = data.query_bytime(sdate, edate)
        elif name == 'query_bykeyword':
            keyword = request.GET.get('keyword', 'get no data')
            msg = data.query_bykeyword(keyword)
        elif name == 'query_bydevice':
            device = request.GET.get('device', 'get no data')
            msg = data.query_bydevice(device)
        elif name == 'query_bylevel':
            level = request.GET.get('level', 'get no data')
            msg = data.query_bylevel(level)
        elif name == 'count_bytype':
            msg = data.count_bytype()
        elif name == 'count_bylevel':
            msg = data.count_bylevel()
        elif name == 'count_device_top5':
            msg = data.count_device_top5()
        elif name == 'count_serious_top10':
            msg = data.count_serious_top10()
        elif name == 'current_all':
            msg = data.current_all()
        elif name == 'ip_config':
            msg = data.get_ip_config()
        elif name == 'port_config':
            msg = data.get_port_config()
        result = {}
        result['name'] = name
        result['msg'] = msg
        result = json.dumps(result)
        return HttpResponse(result)


# 获取客户机传入的POST数据，并进行数据更新
@csrf_exempt
def get_json(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        msg = req['msg']
        name = req['name']
        result = 'ok'
        if name == 'port':
            data.port = msg
        elif name == 'cdrom_exist':
            data.cdrom_exist = msg
        elif name == 'cdrom_state':
            data.cdrom_state = msg
        elif name == 'sysinfo':
            data.sysinfo = msg
        elif name == 'user':
            data.user = msg
        elif name == 'usb':
            data.usb = msg
        elif name == 'ip':
            data.ip = msg
        elif name == 'serial':
            data.serial = msg
        elif name == 'parallel':
            data.parallel = msg
        elif name == 'ip_config':
            result = data.get_ip_config()
        elif name == 'port_config':
            result = data.get_port_config()
        elif name == 'query_usb':
            result = data.query_usb(msg)
        elif name == 'prt_error':
            result = data.prt_error(msg)
        return HttpResponse(result)
