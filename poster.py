#!/usr/bin/python
# -*- coding:utf-8 -*-
"""A simple poster for use Github Pages as Blog"""
import sys
import os
import re
import datetime
import shutil
import markdown2

reload(sys)
sys.setdefaultencoding('utf-8')
LAYOUT_PATH='.layout'
DEFAULT_LAYOUT='default.layout'

MD_PATH='.posts'
POST_PATH='posts'

INDEX='.id'

DATE_FMT='%Y-%m-%d'

HOME='index.html'


def _check_env():
	return os.path.isfile(INDEX) and os.path.exists(MD_PATH) and os.path.exists(LAYOUT_PATH)

def init():
	"""
	init github pages
	
	"""
	if not os.path.exists(HOME):
		with open(HOME,'w') as home:
			home.write('\n'.join([
			'<!DOCTYPE html>',
			'<html>',
			'<head>',
			'<meta charset="utf-8"/>',
			'<meta http-equiv="X-UA-Compatible" content="chrome=1"/>',
			'<title>Home Page</title>',
			'</head>',
			'<body>',
			'<h1>Home Page</h1>',
			'<!--{contents-start}-->',
			'<!--{contents-end}-->',
			'</body>',
			'</html>',
			]))
	else:
		print '[!] %s exists\n' % HOME
		print 'if you want generate contents, please insert'
		print '\t<!--{contents-start}-->'
		print '\t<!--{contents-end}}-->'
		print 'in %s' % HOME
	if not os.path.exists(LAYOUT_PATH):
		os.makedirs(LAYOUT_PATH)
	layout_file = os.path.join(LAYOUT_PATH, DEFAULT_LAYOUT)
	if not os.path.isfile(layout_file):
		with open(layout_file,'w') as layout:
			layout.write('\n'.join([
			'<!DOCTYPE html>',
			'<html>',
			'<head>',
			'<meta charset="utf-8"/>',
			'<meta http-equiv="X-UA-Compatible" content="chrome=1"/>',
			'<!-- css -->',
			'<!-- title -->',
			'<title>{title}</title>',
			'</head>',
			'<body>',
			'<!-- content -->',
			'{content}',
			'</body>',
			'</html>',
			'',
			]))
	if not os.path.exists(MD_PATH):
		os.makedirs(MD_PATH)
	if not os.path.exists(INDEX):
		with open(INDEX,'w') as idfile:
			idfile.write('\n'.join([
			'#0',		# 保存最大索引
			'',
			]))


def clear():
	"""
	clear
	"""
	flag=raw_input('Will remove generated files,continue?[Y/N]:')
	if flag != 'Y' and flag != 'y':
		return
	if os.path.exists(LAYOUT_PATH):
		shutil.rmtree(LAYOUT_PATH)
	if os.path.exists(MD_PATH):
		shutil.rmtree(MD_PATH)
	if os.path.exists(POST_PATH):
		shutil.rmtree(POST_PATH)
	if os.path.isfile(INDEX):
		os.remove(INDEX)


def list(title=None, date=None):
	"""
	list all the blogs
	:param title: blog title
	:param date:  blog created/modified date
	:return
	"""
	if not os.path.isfile(INDEX):
		print '%s not found' % INDEX
		return
	ret={}
	with open(INDEX) as id:
		for line in id:
			line=line.rstrip()
			if line and not line.startswith('#') and not line.startswith('-'):
				token=line.split()
				_id = int(token[0])
				_title=token[1]
				_date=token[2]
				if title is not None:
					if _title==title:
						if date is not None:
							if _date==date:
								ret[_id]=(_title, _date)
						else:
							ret[_id]=(_title, _date)
				else:
					ret[_id]=(_title, _date)
	for k, v in ret.items():
		print '%d\t%20s\t[%s]' % (k, v[0], v[1])
	return ret if ret else None


def create(title, date):
	"""
	create a new blog
	:param title: blog's title
	:param date:  created date
	:return
	"""
	if not title:
		print '[!] title is required\n\n'
		usage()
	if not date:
		date = datetime.datetime.now().strftime(DATE_FMT)
	r = list(title, date)	
	if r is not None:
		print '[!] create %s %s fail, it has exists\n\n' % (title, date)
		usage(False)
	if not os.path.exists(os.path.join(MD_PATH, date)):
		os.makedirs(os.path.join(MD_PATH, date))
	with open(os.path.join(MD_PATH, date, '%s.md'%title), 'w') as post:
		post.write('<!-- default -->')
		with open(INDEX, 'r+') as idfile:
			idx=int(idfile.readline()[1:])
			id_info=['#%d'%(idx+1),]
			for line in idfile:
				id_info.append(line.rstrip())
			id_info.append('+%d %s %s' % (idx, title, date))
			idfile.seek(0)
			idfile.truncate(0)
			idfile.write('\n'.join(id_info))


	
def remove(title, date):
	"""
	remove blog
	:param title: blog's title
	:param date: blog created/modified date
	:return
	"""
	if not title:
		print '[!] title is required\n\n'
		usage()
	ret = list(title, date)
	if not ret:
		print '[!] %s %s not exists\n\n'%(title, date)
		usage(False)
	_id = None
	_title, _date = None, None
	if len(ret)>1:
		try:
			_id = int(raw_input('input id:'))
			_title, _date = ret[_id]
		except (ValueError, KeyError):
			print '[!] invalid id\n\n'
			usage()
	else:
		k, v = ret.items()[0]
		_id = k
		_title, _date = v
	if raw_input('[?] continue to remove %s %s [Y/N]:'%(_title, _date)).upper()!='Y':
		usage(False)
	with open(INDEX,'r+') as idfile:
		buf = []	
		for line in idfile:
			if not line.startswith('#') and int(line.lstrip().split()[0]) == _id:
				buf.append(('-'+line[1:]).rstrip('\n'))
			else:
				buf.append(line.rstrip('\n'))
		idfile.seek(0)
		idfile.truncate(0)
		idfile.write('\n'.join(buf))
	
	

def build():
	"""
	md生成html
	更新index.html目录
	"""
	def mk2html(title, date):
		if not os.path.exists(os.path.join(POST_PATH, date)):
			os.makedirs(os.path.join(POST_PATH, date))
		with open(os.path.join(MD_PATH, date, '%s.md'%title)) as md:
			_layout = md.readline().replace('<!--','').replace('-->','').strip()
			if not os.path.exists(os.path.join(LAYOUT_PATH,'%s.layout'%_layout)):
				print '[!] layout %s not exists' % _layout
				return False
			else:
				with open(os.path.join(LAYOUT_PATH, '%s.layout'%_layout)) as _layout_file:
					with open(os.path.join(POST_PATH, date, '%s.html'%title), 'w') as html:
						html.write(_layout_file.read().format(content=markdown2.markdown(md.read()), title=title))
						return True
		return False
		
	re_text='\s*<\s*!--\s*\{\s*contents-start\s*\}\s*-->\s*\n((.|\n)*)\s*<\s*!--\s*\{\s*contents-end\s*\}\s*-->'
	with open(HOME,'r+') as home:
		dom = home.read()
		new_contents = []
		with open(INDEX, 'r+') as index_file:
			buf = []
			for line in index_file:
				if line and not line.startswith('#'):
					_id, _title, _date = tuple(line[1:].split())
					if line.startswith('+'):							
						if mk2html(_title, _date):
							buf.append((' '+line[1:]).rstrip('\n'))
						else:
							buf.append(line.rstrip('\n'))
						new_contents.append((_title, _date))
					elif line.startswith('-'):
						buf.append(line.rstrip('\n'))
					elif line.startswith(' '):
						buf.append(line.rstrip('\n'))
						new_contents.append((_title, _date))
				elif line.startswith('#'):
					buf.append(line.rstrip('\n'))
			index_file.seek(0)
			index_file.truncate(0)
			index_file.write('\n'.join(buf))
		m = re.search(re_text, dom)
		if m and new_contents:
			content_start = m.start(1)
			content_end = m.end(1)
			before = dom[:content_start]
			after = dom[content_end:]
			home.seek(0)
			home.truncate(0)
			home.write(before)
			home.write('<!--{contents-start}-->\n')
			home.write('<ul>\n')
			home.write('\n'.join(['<li><a href="posts/{date}/{title}.html" target="_blank">{title} [{date}]</a></li>'.format(title=title, date=date) for title, date in new_contents]))
			home.write('\n</ul>\n')
			home.write('<!--{contents-end}-->')
			home.write(after)

	
def usage(display=True):
	"""
	print usage and exit
	"""
	usage = [
		'Usage:',
		'\tpython poster action title [date]',
		'',
		'action list:'
		'',
		'\tinit: init github pages',
		'\tclear: clear generated files',
		'\tcreate title [date]: create new blog',
		'\tremove title [date]: remove exist blog',
		'\tlist [title] [date]: list blog',
		'\tbuild: markdown to html',
	]
	if display:
		print '\n'.join(usage)
	sys.exit(1)

if __name__ == '__main__':
	if len(sys.argv)>=2 and sys.argv[1] == 'init':
		init()
	elif len(sys.argv)>=2 and sys.argv[1] == 'clear':
		clear()
	elif len(sys.argv)>=2 and sys.argv[1] == 'build':
		build()
	elif len(sys.argv)>=2 and (sys.argv[1] != 'init' and sys.argv[1] != 'clear'):
		action = sys.argv[1]
		if action == '_check_env':
			usage()
		if not _check_env():
			print '[!] need init first\n\n'
			usage()
		title = None
		date = None
		if len(sys.argv)>=3:
			title = sys.argv[2]
		if len(sys.argv)>=4:
			date = sys.argv[3]
		try:
			datetime.datetime.strptime(date, DATE_FMT)
		except (ValueError, TypeError) :
			date = None
		try:
			globals()[action](title, date)
		except KeyError:
			usage()
	else:
		usage()

	
