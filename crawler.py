'''
   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   any later version.
   
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
   
   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from HTMLParser import HTMLParser
from urllib2 import urlopen

import StringIO
import cStringIO

import sys

import sqlite3

class Spider(HTMLParser):
	divTagCount = 0
	tdTagCount = 0
	poslistOfProjects = None
	closeListOfProjects = False
	project = None
	nameProject = False
	countPartsNameProject = 0
	brTagCount = 0
	labels = False
	label = False
	listPages = False
	linkPage = False
	pageHref = None
	textCountProjects = False
	tdTagCountTextCountProjects = 0
	
	#Save data
	number_projects = 0
	listProjects = []
	projectTemp = {}
	listLabels = []
	labelTemp = {}
	nextPage = None
	
	def __init__(self, url):
		self.divTagCount = 0
		self.tdTagCount = 0
		self.poslistOfProjects = None
		self.closeListOfProjects = False
		self.project = None
		self.nameProject = False
		self.countPartsNameProject = 0
		self.brTagCount = 0
		self.labels = False
		self.label = False
		self.listPages = False
		self.linkPage = False
		self.pageHref = None
		self.textCountProjects = False
		self.tdTagCountTextCountProjects = 0
		self.number_projects = 0
		self.listProjects = []
		self.projectTemp = {}
		self.listLabels = []
		self.labelTemp = {}
		self.nextPage = None
		
		HTMLParser.__init__(self)
		try:
			req = urlopen(url)
			self.feed(req.read())
		except:
			self.errorUrl = True
			print("Error")
		else:
			self.errorUrl = False
	
	def handle_starttag(self, tag, attrs):
		attrsDict = dict(attrs)
		
		if tag == 'div':
			if not self.closeListOfProjects:
				self.divTagCount += 1
				if 'id' in attrsDict:
					if attrsDict['id'] == 'serp':
						self.poslistOfProjects = self.divTagCount
			else:
				self.listPages = True
		
		if tag == 'table':
			if self.poslistOfProjects != None:
				self.project = True
			else:
				if 'class' in attrsDict:
					if attrsDict['class'] == 'mainhdr':
						self.textCountProjects = True
			
		if tag == 'td':
			if self.project:
				self.tdTagCount += 1
			if self.textCountProjects:
				self.tdTagCountTextCountProjects += 1
			
		if tag == 'a':
			if self.listPages:
				if 'href' in attrsDict:
					self.linkPage = True
					self.pageHref = attrsDict['href']
			elif self.labels:
				if 'href' in attrsDict:
					self.labelTemp['href'] = attrsDict['href']
					print 'label href->' + self.labelTemp['href']
					self.label = True
			elif self.tdTagCount == 2:
				self.nameProject = True
				if 'href' in attrsDict:
					self.projectTemp['href'] = attrsDict['href']
					print 'href->' + self.projectTemp['href']
			else:
				self.nameProject = False
		
		if tag == 'span' and self.project:
			if 'class' in attrsDict:
				if attrsDict['class'] == 'labels':
					self.labels = True
	
	def handle_startendtag(self, tag, attrs):
		if tag == 'br' and self.project:
			self.brTagCount += 1
	
	def handle_endtag(self, tag):
		if tag == 'div':
			if self.divTagCount == self.poslistOfProjects:
				self.poslistOfProjects = None
				self.closeListOfProjects = True
			self.divTagCount -= 1
			self.listPages = False
					
		if tag == 'table':
			print '-------------------------------------'
			self.textCountProjects = False
			self.project = False
			self.tdTagCount = 0
			self.nameProject = False
			self.countPartsNameProject = 0
			self.brTagCount = 0
			
			if self.projectTemp:
				self.listProjects.append(self.projectTemp)
				self.projectTemp = {}
			
		if tag == 'span' and self.labels:
			self.labels = False
			
			self.projectTemp['labels'] = self.listLabels
			self.listLabels = []
			self.labelTemp = {}
			
		if tag == 'a':
			self.label = False
			if self.linkPage:
				self.linkPage = False
	
	def handle_data(self, data):
		if self.textCountProjects:
			if self.tdTagCountTextCountProjects == 2:
				text = data.strip()
				chunks = text.split('of')
				self.number_projects = str(chunks[1]).strip()
				print 'number_projects->' + self.number_projects
				self.textCountProjects = False
		
		if self.nameProject:
			self.countPartsNameProject += 1
			
			if self.countPartsNameProject == 1:
				self.projectTemp['id'] = data.strip()
				print 'id->' + self.projectTemp['id']
			if self.countPartsNameProject == 3:
				self.projectTemp['name'] = data.strip()
				print 'name->' + self.projectTemp['name']
		
		if self.project:
			if self.brTagCount == 2:
				self.projectTemp['description'] = data.strip()
				print 'description->' + self.projectTemp['description']
		
		if self.labels:
			if self.label:
				self.labelTemp['name'] = data.strip()
				print 'label name->' + self.labelTemp['name']
				self.listLabels.append(self.labelTemp)
				self.labelTemp = {}
				
		if self.listPages:
			if self.linkPage and data.strip() == 'Next':
				self.nextPage = self.pageHref
				print 'page next href->' + self.nextPage



def main():
	urlTemp = url = 'http://code.google.com/hosting/search'
	scan = True
	listProjects = []
	count = 0
	tries = 0
	
	db = sqlite3.connect('crawler.db')
	cur = db.cursor()
	
	while scan:
		count += 1
		print("Page %d" % count)
		
		old_stdout = sys.stdout
		sys.stdout = cStringIO.StringIO()
		
		spider = Spider(urlTemp)
		
		outputData = sys.stdout.getvalue()
		sys.stdout = old_stdout 
		
		if spider.errorUrl:
			print("Error url: %s" % urlTemp)
			tries += 1
			count -= 1
			print("Try %d" % tries)
			if tries > 10:
				break
			else:
				continue
		else:
			tries = 0
			listProjects = listProjects + spider.listProjects
		
		if spider.nextPage:
			urlTemp = url.replace('search', spider.nextPage)
		else:
			break
		
		number_projects = spider.number_projects
		spider = None
	
	
	cur.execute('SELECT * FROM google_code WHERE type = "number_projects";');
	rows = cur.fetchall()
	if not rows:
		cur.execute('INSERT INTO google_code(type, value) values ("number_projects", "' + number_projects + '")');
	else:
		cur.execute('UPDATE google_code SET value = "' + number_projects + '" WHERE type = "number_projects"');
	db.commit()
	
	count = 0
	for project in listProjects:
		count += 1
		print ("Project %d" % count)
		
		cur.execute('SELECT * FROM project WHERE id_in_google = "' + project['id'] + '"')
		project_row = cur.fetchall()
		
		if not project_row:
			#sql = 'INSERT INTO project(id_in_google, href, name, description)' + \
			#	'values ("' + project['id'] + '", "' + project['href'] + '", "' + project['name'] + '", "' + project['description'] + '")'
			sql = 'INSERT INTO project(id_in_google, href, name)' + \
				'values ("' + project['id'] + '", "' + project['href'] + '", "' + project['name'] + '")'
			cur.execute(sql);
			db.commit()
		else:
			pass
			#cur.execute('UPDATE google_code SET "' + number_projects + '" WHERE type = "number_projects"');
			
		for label in project['labels']:
			cur.execute('SELECT id FROM project WHERE id_in_google = "' + project['id'] + '"')
			project_id = cur.fetchall()
			project_id = project_id[0][0]
			cur.execute('SELECT id FROM labels WHERE label = "' + label['name'] + '"')
			label_id = cur.fetchall()
			
			if not label_id:
				sql = 'INSERT INTO labels(label, href) values ("' + label['name'] + '", "' + label['href'] + '")' 
				cur.execute(sql);
				db.commit()
				label_id = cur.lastrowid
			else:
				label_id = label_id[0][0]
			
			cur.execute('SELECT id FROM project_labels WHERE id_label = ' + str(label_id) + ' AND id_project = ' + str(project_id))
			project_label_id = cur.fetchall()
			
			if not project_label_id:
				sql = 'INSERT INTO project_labels(id_label, id_project) values (' + str(label_id) + ', ' + str(project_id) + ')' 
				cur.execute(sql)
				db.commit()
	
	sql = 'CREATE TABLE labels_count AS SELECT t1.id, t1.label, ' + \
		'	(SELECT COUNT(t2.id) FROM project_labels AS t2 ' + \
		'		WHERE t2.id_label = t1.id) AS count ' + \
		'	FROM labels AS t1' + \
		'	ORDER BY label ASC;';
	cur.execute(sql)
	db.commit()
	
	db.close()

if __name__ == '__main__':
	main()
