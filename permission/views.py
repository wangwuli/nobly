from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
# Create your views here.
# from reception.models import index
from django.contrib.auth.models import User,Permission,Group


def useraddr():
	username = request.POST.get('username')
	password = request.POST.get('password')
	mail = request.POST.get('mail')	
	try:
		User.objects.create_user(username,mail,password).save()
	#User.objects.create_user(username,mail,password)
	except:
		print('用户已存在')

def grouaddruser():	
	usernamei = request.POST.get('username')
	group = request.POST.get('group')
	userobject = User.objects.get(username=usernamei)
	usergroup = userobject.groups.add(group)
	

#获取组对象
#u = User.objects.get(username='alice')
#alice_group = User.groups.through.objects.get(user=u)
#更改用户组
#alice_group.group = manager
#alice_group.save()
	

def permissioninquire():     #是否有模块的权限
	username = request.POST.get('username')
	modeapp = request.POST.get('modeapp')
	
	username.has_perm('%s_permission' %modeapp)
	return HttpResponse('123')
#alice.has_perm('apps.reception')   ？？？
#False
	
	
def permissioninquire2():
	usernamei = request.POST.get('username')
	usernamei=User.objects.get(username=usernamei)
	usernamei.user_permissions.all()           #查询用户权限
	usernamei.groups.all()                         #查询组权限
	
	#usernamei.user_permissions                 #？？？？
	#alice.groups.all()[0].permissions.all()     #？？？？
	
def permissionindex():         #创建新权限
	modeapp = request.POST.get('modeapp')
	content_type = ContentType.objects.get_for_model(modeapp)   #？？？
	permission = Permission.objects.create(
	codename=('%s_permission' %modeapp),
	name=('%s_permission_posts' %modeapp),
    content_type=content_type
	)
	
	return HttpResponse('123')
	
def permissionuser():          #给用户权限操作
	what = request.POST.get('what')
	username = request.POST.get('username')
	permissioni = request.POST.get('permissioni')
	
	if what == 1:              #添加用户权限
		username.permission.add(permissioni,)
	# elif what == 2:            #重设用户权限
		# username.permission.set([permissionilist])
	elif what == 3:            #移除用户权限
		username.permission.remove(permissioni,)
	elif what == 4:            #清空用户权限
		username.permission.clear()


def permissiongroup():          #给用户组权限操作
	what = request.POST.get('what')
	username = request.POST.get('username')
	permissioni = request.POST.get('permissioni')
		
	if what == 1:              #添加用户组权限
		username.groups.add(permissioni,)
	# elif what == 2:          #重设用户权限
		# username.groups.set([permissioni])
	elif what == 3:            #移除用户组权限
		username.groups.remove(permissioni,)
	elif what == 4:            #清空用户组权限
		username.groups.clear()