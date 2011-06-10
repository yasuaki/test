from django.db import models
from django.contrib.sites.models import Site

# Create your models here.

class Cpu(models.Model):
	name = models.CharField(max_length=30)
	abb = models.CharField(max_length=8)
	site = models.ForeignKey(Site)

	def __unicode__(self):
		return self.name

class Si(models.Model):
	ver = models.CharField(max_length=30)
	title = models.CharField(max_length=128)
	base_ver = models.ForeignKey("self", blank=True, null=True)
	site = models.ForeignKey(Site)
	cpu = models.ForeignKey(Cpu)
	git_branch = models.CharField(max_length=128)
	git_tag = models.CharField(max_length=128, blank=True, null=True)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField(blank=True, null=True)

	def __unicode__(self):
		return self.ver

	class Meta:
		unique_together = ("cpu", "ver")

class Fbu(models.Model):
	name = models.CharField(max_length=30)
	abb = models.CharField(max_length=8)
	site = models.ForeignKey(Site)

	def __unicode__(self):
		return self.name

class SiAttendFbu(models.Model):
	si = models.ForeignKey("Si")
	fbu = models.ForeignKey(Fbu)
	relcnt_major = models.IntegerField(default=0)
	relcnt_minor = models.IntegerField(default=0)
	valid = models.BooleanField(default=True)
	site = models.ForeignKey(Site)

	class Meta:
		unique_together = ("si", "fbu")

SI_PHASES = (
	(u'FR', u'FBU Release'),
	(u'DL', u'Download'),
	(u'CO', u'Compile'),
	(u'BC', u'Base Check'),
	(u'FC', u'FBU Check'),
	(u'SC', u'Ship Check'),
	(u'SR', u'SBU Release'),
)

SI_STATUS = (
	(u'OK', u'OK'),
	(u'ER', u'Error'),
	(u'DL', u'Delay'),
	(u'PG', u'Progress'),
)

class SiPhaseStatus(models.Model):
	si = models.ForeignKey(Si)
	fbu = models.ForeignKey(Fbu)
	phase = models.CharField(max_length=2, choices=SI_PHASES)
	status = models.CharField(max_length=2, choices=SI_STATUS)
	upd_date = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = ("si", "fbu", "phase")
