from django.conf.urls import url
from . import views

# from django.conf.urls.static import static
# from django.conf import settings

urlpatterns = [
	url(r'^index/$', views.index, name='index'),
    url(r'^getdata/$', views.getdata, name='getdata'),
	url(r'^getineargraph$', views.getineargraph, name='getineargraph'),
	url(r'^gethostchart$', views.gethostchart, name='gethostchart'),
	url(r'^givehostdata$', views.givehostdata, name='givehostdata'),
]