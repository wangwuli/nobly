from django.conf.urls import url
from . import views

# from django.conf.urls.static import static
# from django.conf import settings

urlpatterns = [
	url(r'^$', views.login, name='login'),
    # url(r'^getdata/$', views.getdata, name='getdata'),
	url(r'^loginsubmit$', views.loginsubmit, name='loginsubmit'),
]
