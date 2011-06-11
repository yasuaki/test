from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns("mysite.si.views",
    url(r'^$', "index", name="si"),
    url(r'^(?P<cpu_name>[^/]+)/(?P<ver>[^/]+)/$', "detail", name="si_detail"),
)
