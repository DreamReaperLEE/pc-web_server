# *_*coding:utf-8 *_*
import time
import json
import MySQLdb

conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='check', port=3306, charset="utf8")
cur = conn.cursor()
# 初始化数据，将实时信息存在内存中
#端口列表
port = []
#驱动器状态
cdrom_exist = ''
cdrom_state = ''
#系统状态
sysinfo = []
#用户列表
user = []
#usb设备列表
usb = []
#IP列表
ip = []
#串口占用列表
serial = []
#并口占用列表
parallel = []

#返回ip白名单
def get_ip_config():
    result=[]
    f = open("D:/python_workplace/pc-status-supervision/web_server/ip_config.txt")
    line = f.readline()
    line = f.readline()
    while line:
        line = line.strip('\n')
        result.append(line)
        line = f.readline()
    data = {}
    data['result'] = result
    data = json.dumps(data)
    return data
#返回端口黑名单
def get_port_config():
    result=[]
    f = open("D:/python_workplace/pc-status-supervision/web_server/port_config.txt")
    line = f.readline()
    line = f.readline()
    while line:
        line = line.strip('\n')
        result.append(line)
        line = f.readline()
    data = {}
    data['result'] = result
    data = json.dumps(data)
    return data

# 返回所有日志信息
def query_all():
    try:
        cur.execute("select * from pc_error order by auto_id DESC limit 500")
        rows = cur.fetchall()
        return rows
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


# 返回按时间查询的日志信息
def query_bytime(sdate, edate):
    try:
        cur.execute(("select * from pc_error where date >='%s' and date<='%s' order by auto_id DESC limit 500") % (sdate, edate))
        rows = cur.fetchall()
        return rows
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


# 返回按关键字查询的日志信息
def query_bykeyword(keyword):
    try:
        cur.execute(
            ("select * from pc_error where concat(device_name,level,type,type_detail,date,time, msg) like '%s%s%s' order by auto_id DESC limit 500") % (
                '%', keyword, '%'))
        rows = cur.fetchall()
        return rows
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


# 返回按设备名称查询的日志信息
def query_bydevice(device):
    try:
        cur.execute(("select * from pc_error where device_name like '%s%s%s' order by auto_id DESC limit 500") % ('%', device, '%'))
        rows = cur.fetchall()
        return rows
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


# 返回按告警等级查询的日志信息
def query_bylevel(level):
    try:
        cur.execute(("select * from pc_error where level='%s' order by auto_id DESC limit 500") % (level))
        rows = cur.fetchall()
        return rows
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


# 返回按类型统计的日志数量
def count_bytype():
    try:
        cur.execute("select type,type_detail,  count(1) AS counts FROM pc_error GROUP BY type_detail")
        rows = cur.fetchall()
        return rows
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


# 返回按告警等级统计的日志数量
def count_bylevel():
    try:
        cur.execute("select level,  count(1) AS counts FROM pc_error GROUP BY level")
        rows = cur.fetchall()
        return rows
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


# 返回按日志详细类型统计的日志数量
def count_device_top5():
    try:
        cur.execute("select *,  count(1) AS counts FROM pc_error  group by type_detail order by count(1) DESC")
        rows = cur.fetchall()
        return rows
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


# 返回最近的十条严重警告数据
def count_serious_top10():
    try:
        cur.execute("select * from pc_error order by level DESC,date DESC limit 10")
        rows = cur.fetchall()
        return rows
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

#根据PID VID查询USB详细信息
def query_usb(data):
    try:
        cur.execute("select * from usb where vid= '%s' and pid = '%s' " % \
                    (data['vid'], data['pid']))
        rows = cur.fetchall()
        if rows:
            every = rows[0]
        else:
            every = [data['vid'], 'unknow', data['pid'], 'unknow']
        result = "vid:{%s}device info:{%s}pid:{%s}product info:{%s}" % (every[3], every[1], every[2], every[0])
        return result
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

# 将日志信息存入数据库，传入PC名称、日志等级、日志大类、日志类型、日志内容
def prt_error(data):
    try:
        gdate = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        gtime = time.strftime('%H:%M:%S', time.localtime(time.time()))
        cur.execute("insert into pc_error value ('%s','%s','%s','%s','%s','%s','%s')" % (
            data['hostname'], data['level'], data['type'], data['detail'], gdate, gtime, data['msg']))
        return 'ok'
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


#当前机器状态概览，返回状态的简易参数
def current_all():
    result={}
    result['port']=len(port)
    cdrom=[]
    cdrom.append(cdrom_exist)
    cdrom.append(cdrom_state)
    result['cdrom']=cdrom
    result['sysinfo']=sysinfo
    result['user']=len(user)
    result['usb']=len(usb)
    result['ip']=len(ip)
    result['serial']=len(serial)
    result['parallel']=len(parallel)
    return result


