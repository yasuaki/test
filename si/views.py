# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response
from mysite.si.models import *
from mysite.si.git_util import get_git_hist

def index(request):
	si = Si.objects.filter(end_date__isnull=True).order_by('start_date')[0]
	return HttpResponseRedirect(reverse('si_detail', kwargs={'cpu_name':si.cpu.name, 'ver':si.ver}))

def detail(request, cpu_name, ver):
	gitdir = "/home/narita/pinax-env/mysite/.git"
	cpu = Cpu.objects.filter(name=cpu_name)[0]
	si = Si.objects.filter(cpu=cpu.id, ver=ver)[0]
	cpu_list = Cpu.objects.order_by('name')
	si_list = Si.objects.filter(cpu=cpu.id).order_by('start_date')
	fburel_hist = get_git_hist(gitdir,si.git_branch,si.git_branch)
	return render_to_response('si/detail.html', {'cpu':cpu, 'si':si, 'cpu_list':cpu_list, 'si_list':si_list, 'fburel_hist':fburel_hist}, context_instance=RequestContext(request))
