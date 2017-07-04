# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from reception.models import HostsInformation, HostsWholesale, HostsConfigwarning, HostsWhowarning, HostsWhowarningAll, HostsWhoerror, HostsNormalAll,HostsWhoerrorAll,HostsNormal
from django.core.cache import cache
# from django.conf import settings
# from django.shortcuts import redirect
from django.http import HttpResponseRedirect
import json
from django.db.models import Max
import datetime


# Create your views here.
def index(request):  # 登录主页
    if request.user.is_authenticated:
        ip_group_list = {}
        hostall = HostsInformation.objects.all()
        for hosts in hostall:
            try:
                ip_group_list[hosts.group].append(hosts.ip)
            except:
                ip_group_list[hosts.group] = [hosts.ip]

        title_name = '监控页面'
        context = {'title_name': title_name, 'ip_group_list': ip_group_list}
        return render(request, 'reception/index.html', context)
    else:
        return render(request, 'reception/login.html')


def getineargraph(request):  # JS数据请求主页数据
	ip = request.POST.get('link')
	if request.user.is_authenticated:		
		
		error_numbel = len(HostsWhoerror.objects.all())
		warning_numbel = len(HostsWhowarning.objects.all())
		normal_numbel = len(HostsNormal.objects.all())
		All_numbel= len(HostsInformation.objects.all())  
		
		new_error = error_numbel
		new_warning = warning_numbel
		new_normal = normal_numbel
		
		today=datetime.date.today()
		month=datetime.timedelta(days=30)
		lastmonth = today - month
		
		time_start = lastmonth.strftime("%Y-%m-%d")   
		time_end = today.strftime("%Y-%m-%d")
		
		warning_all_object = HostsWhowarningAll.objects.filter(newtime__range=(lastmonth,today))
		error_all_object = HostsWhoerror.objects.filter(newtime__range=(lastmonth,today))
		Normal_all_object = HostsNormalAll.objects.filter(newtime__range=(lastmonth,today))
		
		data_string = []
		for A in range(30):
			data_string_one = []
			time_swap=datetime.timedelta(days=A)
			time_new = lastmonth + time_swap
			
			
			try:
				data_string_one.append(len(error_all_object.filter(newtime=time_new)))
			except:
				data_string_one.append('N')
			
			try:
				data_string_one.append(len(Normal_all_object.filter(newtime=time_new)))
			except:
				data_string_one.append('N')
				
			try:
				data_string_one.append(len(warning_all_object.filter(newtime=time_new)))
			except:
				data_string_one.append('N')
			
			A += 1
			
			data_string.append(data_string_one)
			
		
		context = {'new_error': new_error, 'new_warning': new_warning,'new_normal':new_normal,'time_start':time_start,'time_end':time_end,'data_string':json.dumps(data_string)}
		
		return render(request, 'reception/nightingale.html',context)
	else:
		return HttpResponse(json.dumps("error"))  # 返回给js的数据


def gethostchart(request):  # 主机监控页面返回
    ipa = request.GET.get('link')
    if request.user.is_authenticated:
        try:
            hostint = HostsInformation.objects.get(ip=ipa)
            CPUnumber = int(hostint.cpu.split(' ')[1].split('threading')[0]) * 100  # CPU数量
            memmorynumber = float(hostint.memmory.split('G')[0])  # 内存单位G
            disknumber = int(hostint.disk.split('G')[0]) / 1000  # 硬盘单位T
            bandwidthnumber = int(hostint.bandwidth)  # 单位MB
        except:
            CPUnumber, memmorynumber, disknumber, bandwidthnumber = 0, 0, 0, 0

        context = {'host_ip': ipa, 'host_cpu': hostint.cpu, 'host_disk': hostint.disk, 'host_memory': hostint.memmory,'host_bandwidth': hostint.bandwidth, 'CPUnumber': CPUnumber, 'memmorynumber': memmorynumber,'disknumber': disknumber, 'bandwidthnumber': bandwidthnumber}
        return render(request, 'reception/host.html', context)
    else:
        return HttpResponse(json.dumps("error"))  # 返回给js的数据


def getmedict(stringA):  # 分割A=1,B=2字符格式并生成字典返回
    dictnetsPeed = {}
    dictnetsswap = stringA.split(',')
    for netsPeedsw in dictnetsswap:
        netsPeedswa = netsPeedsw.split('=')
        dictnetsPeed[netsPeedswa[0]] = netsPeedswa[1]
    return dictnetsPeed

	
def Wheretowrite(signal,hoSt,new_time,new_disk,new_bandwidth,new_memmory,new_cpu):  
	X = [HostsWhowarningAll,HostsNormalAll,HostsWhoerrorAll]
	for S in X:
		if S == signal:
			Ss = S.objects.filter(ip=hoSt,newtime=new_time).update(disk=new_disk, bandwidth=new_bandwidth,memmory=new_memmory, cpu=new_cpu)
			if not Ss:
				S_information = S(ip=hoSt, disk=new_time, bandwidth=new_bandwidth,memmory=new_memmory, cpu=new_cpu, newtime=new_time)
				S_information.save()
		else:
			S.objects.filter(ip=hoSt,newtime=new_time).delete()
			
def Wheretowriteone(signal,hoSt,new_time,new_disk,new_bandwidth,new_memmory,new_cpu): 	
	Y = [HostsWhowarning,HostsNormal,HostsWhoerror]
	for L in Y:
		if L == signal:
			Ll = L.objects.filter(ip=hoSt).update(disk=new_time, bandwidth=new_bandwidth,memmory=new_memmory, cpu=new_cpu, newtime=new_time)
			if not Ll:
				S_information = L(ip=hoSt, disk=new_disk, bandwidth=new_bandwidth,memmory=new_memmory, cpu=new_cpu, newtime=new_time)
				S_information.save()
		else:
			L.objects.filter(ip=hoSt).delete()
		
			

def getdata(request):  # 接收客户端监控信息
	sysTem = request.GET.get('system')
	stAte = request.GET.get('state')
	hoSt = request.GET.get('host')
	cPu = request.GET.get('cpu')
	meMory = request.GET.get('mem')
	netsPeed = request.GET.get('nets')
	diskSize = request.GET.get('disk')
	newTime = request.GET.get('newtime')

    # obj=Hostsinformation.objects.filter(ip=hoSt)
	recordedvalue = 0
	question = {}
	if meMory:  # 没有内存信息参数,进入新增服务器状态记录
		obj = HostsWholesale(ip=hoSt, network=netsPeed, cpu=cPu, mem=meMory, disk=diskSize, newtime=newTime)
		obj.save()

        # redis 缓存
		cachehost = {'network': netsPeed, 'cpu': cPu, 'mem': meMory, 'disk': diskSize, 'newtime': newTime}
		cache.set(hoSt, cachehost, 120)

		
        # 警告判断
		try:
			allconfigwarning = HostsConfigwarning.objects.get(ip=hoSt)
		except:

			allconfigwarning = HostsConfigwarning.objects.get(ip='all')
		finally:

			hostinfo = HostsInformation.objects.get(ip=hoSt)

			dictnetsPeed = getmedict(netsPeed)
            # return HttpResponse('%s' %dictnetsPeed)

			allnetsPeed = int(dictnetsPeed['intraffic']) + int(dictnetsPeed['outtraffic'])
			if allconfigwarning.networkwarning <= allnetsPeed / hostinfo.bandwidth:
				question['bandwidth'] = allnetsPeed / hostinfo.bandwidth
				recordedvalue += 1
			else:
				question['bandwidth'] = 'proper'

			dictmeMory = getmedict(meMory)
			memoryuser = float(dictmeMory['usage'])
			if allconfigwarning.memorywarning <= memoryuser:
				question['memmory'] = memoryuser
				recordedvalue += 1
			else:
				question['memmory'] = 'proper'

            # CPU警告判断
            # return HttpResponse('%s' %cPu)
			listcpu = cPu.strip('[]').split(',')
            # return HttpResponse('%s' %listcpu)
			cpuall = 0
			for cpuone in listcpu:
                # return HttpResponse(cpuall + int(cpuone))
				cpuall = cpuall + float(cpuone.strip())
			if cpuall / len(listcpu) >= allconfigwarning.cpuwarning:
				question['cpu'] = cPu
				recordedvalue += 1
			else:
				question['cpu'] = 'proper'

            # disk警告判断
			listdiskSize = diskSize.split(',')
            # return HttpResponse(listdiskSize)
			diskinfo = []
			for diskone in listdiskSize:
                # return HttpResponse('%s' %listdiskSize)
				try:
					if float(diskone.split('=')[1]) >= allconfigwarning.diskwarning:
						diskinfo.append(diskone)
				except IndexError:
					pass
			if len(diskinfo):
				question['disk'] = diskinfo
				recordedvalue += 1
			else:
				question['disk'] = 'proper'
			
			new_time= datetime.datetime.now().strftime("%Y-%m-%d")
			
			if recordedvalue:       #如果正常recordedvalue值为0
				signal = HostsWhowarningAll
				Wheretowrite(signal,hoSt,new_time,question['disk'], question['bandwidth'], question['memmory'], question['cpu'])
				
				signal2 = HostsWhowarning
				Wheretowriteone(signal2,hoSt,new_time,question['disk'], question['bandwidth'], question['memmory'], question['cpu'])
				
			else:
				signal = HostsNormalAll
				Wheretowrite(signal,hoSt,new_time,question['disk'], question['bandwidth'], question['memmory'], question['cpu'])
				
				signal2 = HostsNormal
				Wheretowriteone(signal2,hoSt,new_time,question['disk'], question['bandwidth'], question['memmory'], question['cpu'])				
					
				
	else:  #添加主机信息
		try:
			obj = HostsInformation.objects.get(ip=hoSt)
		except:
			obj = HostsInformation(ip=hoSt, system=sysTem, state=stAte)
			obj.save()

	return HttpResponse('%s' % question)


def givehostdata(request):  
    if request.user.is_authenticated:
        ipS = request.POST.get('who')

        # getcachehost = {'network':netsPeed,'cpu':cPu,'mem':meMory,'disk':diskSize,'newtime':newTime}
        getcachehost = cache.get(ipS)
        # return HttpResponse(getcachehost)
        NU = 0
        for keysd in getcachehost['cpu'].strip('[]').split(','):
            NU = NU + float(keysd)
        getcachehost['cpu'] = int(NU)

        for keysd in getcachehost['network'].split(','):
            if keysd.split('=')[0] == 'intraffic':
                getcachehost['intraffic'] = keysd.split('=')[1]
            else:
                getcachehost['outtraffic'] = keysd.split('=')[1]
                del getcachehost['network']

        NU = 0
        try:
            for keysd in getcachehost['disk'].split(','):
                NU = NU + int(keysd.split('MB')[0].split('G')[1])
        except ValueError:
            pass
        getcachehost['diskall'] = round(NU / 1000, 2)

        for keysd in getcachehost['mem'].split(','):
            if keysd.split('=')[0] == 'memallMB':
                memallMB = keysd.split('=')[1]
            elif keysd.split('=')[0] == 'free':
                memfree = keysd.split('=')[1]

        getcachehost['memuse'] = int(memallMB) - int(memfree)

        charcachehost = str(getcachehost)




        return HttpResponse(json.dumps(charcachehost))
