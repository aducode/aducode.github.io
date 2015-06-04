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


def list(name=None, date=None):
	"""
	list all the blogs
	:param name: blog name
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
				_name=token[1]
				_date=token[2]
				if name is not None:
					if _name==name:
						if date is not None:
							if _date==date:
								ret[_id]=(_name, _date)
						else:
							ret[_id]=(_name, _date)
				else:
					ret[_id]=(_name, _date)
	for k, v in ret.items():
		print '%d\t%20s\t[%s]' % (k, v[0], v[1])
	return ret if ret else None


def create(name, date, title):
	"""
	create a new blog
	:param name: blog's name
	:param title: blog's title
	:param date:  created date
	:return
	"""
	if not name:
		print '[!] name is required\n\n'
		usage()
	if not date:
		date = datetime.datetime.now().strftime(DATE_FMT)
	if not title:
		title = name
	r = list(name, date)	
	if r is not None:
		print '[!] create %s %s fail, it has exists\n\n' % (name, date)
		usage(False)
	if not os.path.exists(os.path.join(MD_PATH, date)):
		os.makedirs(os.path.join(MD_PATH, date))
	with open(os.path.join(MD_PATH, date, '%s.md'%name), 'w') as post:
		post.write('<!--{layout:default title:%s}-->' % title)
		with open(INDEX, 'r+') as idfile:
			idx=int(idfile.readline()[1:])
			id_info=['#%d'%(idx+1),]
			for line in idfile:
				id_info.append(line.rstrip())
			id_info.append('+%d %s %s' % (idx, name, date))
			idfile.seek(0)
			idfile.truncate(0)
			idfile.write('\n'.join(id_info))


	
def remove(name, date):
	"""
	remove blog
	:param name: blog's name
	:param date: blog created/modified date
	:return
	"""
	if not name:
		print '[!] name is required\n\n'
		usage()
	ret = list(name, date)
	if not ret:
		print '[!] %s %s not exists\n\n'%(name, date)
		usage(False)
	_id = None
	_name, _date = None, None
	if len(ret)>1:
		try:
			_id = int(raw_input('input id:'))
			_name, _date = ret[_id]
		except (ValueError, KeyError):
			print '[!] invalid id\n\n'
			usage()
	else:
		k, v = ret.items()[0]
		_id = k
		_name, _date = v
	if raw_input('[?] continue to remove %s %s [Y/N]:'%(_name, _date)).upper()!='Y':
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
	
	

def build(force_build=False):
	"""
	md生成html
	更新index.html目录
	:param force_build: 是否强制重新转换markdown
	"""
	def mk2html(name, date):
		re_text='\s*<\s*!--\s*\{\s*layout:(.+)\s+title:(.+)\s*\}\s*-->'
		if not os.path.exists(os.path.join(POST_PATH, date)):
			os.makedirs(os.path.join(POST_PATH, date))
		with open(os.path.join(MD_PATH, date, '%s.md'%name)) as md:
			m = re.search(re_text, md.readline())
			_layout = 'default'
			_title = name
			if m:
				_layout=m.group(1)
				_title = m.group(2)
			if not os.path.exists(os.path.join(LAYOUT_PATH,'%s.layout'%_layout)):
				print '[!] layout %s not exists' % _layout
			else:
				with open(os.path.join(LAYOUT_PATH, '%s.layout'%_layout)) as _layout_file:
					with open(os.path.join(POST_PATH, date, '%s.html'%name), 'w') as html:
						html.write(_layout_file.read().format(content=markdown2.markdown(md.read()), title=_title))
						return _title
		
	re_text='\s*<\s*!--\s*\{\s*contents-start\s*\}\s*-->\s*\n((.|\n)*)\s*<\s*!--\s*\{\s*contents-end\s*\}\s*-->'
	with open(HOME,'r+') as home:
		dom = home.read()
		new_contents = []
		with open(INDEX, 'r+') as index_file:
			buf = []
			for line in index_file:
				if line and not line.startswith('#'):
					_id, _name, _date = tuple(line[1:].split())
					if line.startswith('+'):							
						_title = mk2html(_name, _date)
						if _title:
							buf.append((' '+line[1:]).rstrip('\n'))
							new_contents.append((_name, _title, _date))
						else:
							buf.append(line.rstrip('\n'))
					elif line.startswith('-'):
						buf.append(line.rstrip('\n'))
					elif line.startswith(' '):
						if force_build:
							_title = mk2html(_name, _date)
							if _title:
								new_contents.append((_name, _title, _date))
						buf.append(line.rstrip('\n'))
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
			home.write('\n'.join(['<li><a href="posts/{date}/{name}.html" target="_blank">{title} [{date}]</a></li>'.format(name=name, title=title, date=date) for name, title, date in new_contents]))
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
		'\tcreate name [date]: create new blog',
		'\tremove name [date]: remove exist blog',
		'\tlist [name] [date]: list blog',
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
		if len(sys.argv)>=3 and sys.argv[2]=='-f':
			build(True)
		else:
			build()
	elif len(sys.argv)>=2 and sys.argv[1] == 'create':
		name = None
		title = None
		date = None
		if len(sys.argv)>=3:
			name = sys.argv[2].replace(' ', '_').replace('\t', '_')
		if len(sys.argv)>=4:
			date = ys.argv[3]
		if len(sys.argv)>=5:
			title = sys.argv[4]
		create(name, date, title)
	elif len(sys.argv)>=2 and (sys.argv[1] not in ('init', 'clear', 'build', 'create')):
		action = sys.argv[1]
		if action == '_check_env':
			usage()
		if not _check_env():
			print '[!] need init first\n\n'
			usage()
		name = None
		date = None
		if len(sys.argv)>=3:
			name = sys.argv[2]
		if len(sys.argv)>=4:
			date = sys.argv[3]
		try:
			datetime.datetime.strptime(date, DATE_FMT)
		except (ValueError, TypeError) :
			date = None
		try:
			globals()[action](name, date)
		except KeyError:
			usage()
	else:
		usage()

	
