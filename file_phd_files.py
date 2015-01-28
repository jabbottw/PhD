"""
/***************************************************************************
Name                 : Post Processing tool set
Description          : Tool set designed to aid in post processing functions
Date                 : 5/9/2014
copyright            : (C) 2014 by Julian Abbott-Whitley - PhD WFS
email                : jwhitley@phdwellfile.com 
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program has been developed for use by PhD well file services.     *
 *                                                                         *
 ***************************************************************************/
 """

import os
import shutil
import imghdr
from os.path import join, isdir
from os import listdir

d = r'C:\Users\jabbottw\Desktop\co'
def build_dir_dict(d):
    dict = {}
    d = os.walk(r'C:\Users\jabbottw\Desktop\co')
    for i in d:
    s = i[0].split('\\')
    index = s[len(s)-1]
    dict[index] = i[0]
    return dict

def main(d):
    # create folder dictionary
    dict = {}
    for f in folders:
        dict[f[:3]] = f
    
    root = r'H:\ColoradoUpdate\1-Colorado_Greater DJ Basin'
    for f in files:
        try:
            src = os.getcwd() + '\\' + f
            dst = root + '\\' + dict[f[2:5]] + '\\' + f
            shutil.copy(src, dst)
        except:
            print "no folder for %s" % f[2:5]
            
            
            
            
            