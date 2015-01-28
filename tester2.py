'''
Created on Jan 3, 2015

@author: Julian
'''
import os
from os.path import join, isdir
import psycopg2
import site
import cmd

site.addsitedir(r'C:\Users\Julian\workspace\Eclipse\phd\repo\PhD')

from pyIBrowser import *
from pgAccessTool import *


def tiff2pdf(src_file):
    exe =  join(os.path.dirname(os.path.abspath(__file__)), r'davtd221\exe\tiff2pdf.exe')
    os.system('%s -1 %s' % (exe, src_file))
    os.remove(src_file)


