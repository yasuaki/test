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
	atendfbu_list = SiAttendFbu.objects.filter(si=si.id,valid=True)
	fburel_hist = get_git_hist(gitdir,si.git_branch,si.git_branch)
	
	# generate phasestatus_list{atendfbu.id}{phase} = {SIPhaseStatus's row}
	phasestatus_list = {}
	for afbu in atendfbu_list:
		p = {}
		p['FR'] = SiPhaseStatus.objects.filter(si=si.id,fbu=afbu.fbu.id,phase=u'FR')[0]
		p['FC'] = SiPhaseStatus.objects.filter(si=si.id,fbu=afbu.fbu.id,phase=u'FC')[0]
		p['SC'] = SiPhaseStatus.objects.filter(si=si.id,fbu=afbu.fbu.id,phase=u'SC')[0]
		phasestatus_list[afbu.fbu.name] = p
	p = {}
	p['DL'] = SiPhaseStatus.objects.filter(si=si.id,phase=u'DL')[0]
	p['CO'] = SiPhaseStatus.objects.filter(si=si.id,phase=u'CO')[0]
	p['BC'] = SiPhaseStatus.objects.filter(si=si.id,phase=u'BC')[0]
	p['SR'] = SiPhaseStatus.objects.filter(si=si.id,phase=u'SR')[0]
	phasestatus_list[0] = p

	return render_to_response(
		'si/detail.html', {
			'cpu':cpu,
			'si':si,
			'cpu_list':cpu_list,
			'si_list':si_list,
			'atendfbu_list':atendfbu_list,
			'phasestatus_list':phasestatus_list,
			'fburel_hist':fburel_hist,
			'si_phase':SI_PHASES,
		},
		context_instance=RequestContext(request)
	)
