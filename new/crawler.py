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
	
	def __init__(self, url):

def main():
	urlTemp = url = 'http://code.google.com/hosting/search'
	
	scan = True
	count = 0
	
	while scan:
		count += 1
		
		spider = Spider(urlTemp)
		
		pass

if __name__ == '__main__':
	main()