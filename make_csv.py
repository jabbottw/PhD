# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 16:41:58 2015

@author: jabbottw
"""
# Import the os module, for the os.walk function
import os
import pandas as pd
 
def main():
    # Set the directory you want to start from
    dir_list = [r'H:\Final PhD Product Data - Basin Service Areas\1-Colorado_Greater DJ Basin',
		r'H:\Final PhD Product Data - Basin Service Areas\2-Colorado_Mountain Basins',
		r'H:\Final PhD Product Data - Basin Service Areas\3-Colorado & Utah_Uinta-Piceance',
		r'H:\Final PhD Product Data - Basin Service Areas\4-Utah & Colorado_Greater Paradox Basin',
		r'H:\Final PhD Product Data - Basin Service Areas\5-Nevada & Utah_Great Basin']
    for i in dir_list:
        rootDir = i
        path, folder = os.path.split(os.getcwd())
        l = []
	folder = i.split('\\')[2]
	print "Processing: %s" % folder
        for dirName, subdirList, fileList in os.walk(rootDir):
            for fname in fileList:
                api = fname[0:14]
		product = folder
                l.append([api, product, dirName, fname])
    	df = pd.DataFrame(l, columns=['api', 'product', 'path', 'file_name'])
    	df['full_path'] = df['path'] + '\\' + df['file_name']
    	del df['file_name']
    	df['relative_path'] = df['full_path'].str[2:]
    	del df['path']
    	out_file = rootDir + '\\' + folder + '.txt' 
    	df.to_csv(out_file)


if __name__ == "__main__":
    main()