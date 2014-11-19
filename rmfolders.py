

import os
from os.path import join, isdir
from os import listdir
def rm_empty_dirs(root):
     sub_dirs = listdir(root)
     for f in sub_dirs:
             file = join(root, f)
             if isdir(file):
                     try:
                             os.rmdir(file)
                     except:
                             print "----> %s" % f