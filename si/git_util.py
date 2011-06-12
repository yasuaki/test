#!/usr/bin/env python
from subprocess import Popen, PIPE

def get_git_hist(gitdir,branch,range):
	hist = []
	is_notes=False
	info = {}

	p = Popen(["/home/narita/pinax-env/mysite/si/git_tools/log_and_notes.sh",gitdir,branch,range], stdout=PIPE)
	for line in p.stdout:
		if line[:7] == 'commit ':
			is_notes = False
			commit = line[7:-1]

		elif line[:7] == 'Notes (':
			is_notes = True
			info['commit'] = commit

		elif is_notes:
			if line[:9] == '    User:':
				info['User'] = line[9:-1]
			if line[:9] == '    Date:':
				info['Date'] = line[9:-1]
			if line[:8] == '    FBU:':
				info['FBU'] = line[8:-1]
			if line[:12] == '    FileCnt:':
				info['FileCnt'] = line[12:-1]

		if line[:7] == 'commit ':
			if info.has_key('commit'):
				hist.append(info)
				info = {}

	if info.has_key('commit'):
		hist.append(info)
		info = {}

	return hist
