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
import sys
import shutil
from os.path import isdir, join
import psycopg2

def get_db_connection():
    con = psycopg2.connect(database='phd', user='postgres', password='admin', host='localhost', port='5432')
    return con
    
    
def get_folder(state, county_id):
    con = get_db_connection()
    cur = con.cursor()
    sql = """select bsa, county from public.county_list where state = '%s' AND county_id = '%s';""" % (state, county_id)
    cur.execute(sql)
    bsa = cur.fetchall()
    return bsa

def build_dir_list(d=r'H:\\Final PhD Product Data - Basin Service Areas'):
    bas = os.listdir(os.getcwd())
    l = []
    for i in range(0, 5):
        if i < 2:         
            counties = os.listdir(os.getcwd() + '\\' + bas[i])
            for j in counties:
                if j[-3:] != 'lsx':
                    l.append([bas[i], 'colorado', j])
        elif i < 4:
            f = os.getcwd() + '\\' + bas[i] + '\\Colorado'
            if isdir(f):
                counties = os.listdir(f)
                for j in counties:
                        if j[-3:] != 'lsx':
                            l.append([bas[i], 'colorado', j])
            f = os.getcwd() + '\\' + bas[i] + '\\Utah'
            if isdir(f):
                counties = os.listdir(f)
                for j in counties:
                    if j[-3:] != 'lsx':
                        l.append([bas[i], 'utah', j])
        else:
            f = os.getcwd() + '\\' + bas[i] + '\\Nevada'
            if isdir(f):
                counties = os.listdir(f)
                for j in counties:
                    if j[-3:] != 'lsx':
                        l.append([bas[i], 'nevada', j])
            f = os.getcwd() + '\\' + bas[i] + '\\Utah'
            if isdir(f):
                counties = os.listdir(f)      
                for j in counties:
                    if j[-3:] != 'lsx':
                        l.append([bas[i], 'utah', j])
    return l
    
def copy_file(r, f, d):
    out = join(d, f)
    src = join(r, f)   
    print "Input location ---> %s" % src
    print "Output location ---> %s \n\n\n\n" % out
    shutil.copy(src, out)
    os.remove(src)
    

def main(d):   
    print d
    state_dict = {'05' : 'colorado', '43' : 'utah', '27' : 'nevada' }
    bsa_dict = {0 : '1-Colorado_Greater DJ Basin', 1 : '2-Colorado_Mountain Basins', 2 : '3-Colorado & Utah_Uinta-Piceance',
    3 : '4-Utah & Colorado_Greater Paradox Basin', 4 : '5-Nevada & Utah_Great Basin'}
    root = r'H:\Final PhD Product Data - Basin Service Areas'
    files = os.listdir(d)
    for f in files:
        state = f[0:2]
        county_id = f[2:5]
        q = get_folder(state_dict[state], county_id)
        if q:
            print "File: %s" % f
            bsa_folder = q[0][0]
            print "Basin Service Area: %s" % bsa_folder
            county_folder = q[0][1]
            print "County: %s\n" % county_folder
            if bsa_folder == bsa_dict[0] or bsa_folder == bsa_dict[1]:
                out_folder = join(root, bsa_folder)
                o_folder = join(out_folder, county_folder)
                
                if isdir(o_folder):
                    copy_file(d, f, o_folder)
            else:
                out_folder = join(root, bsa_folder)
                ou_folder = join(out_folder, state_dict[state].capitalize())
                o_folder = join(ou_folder, county_folder)
                if isdir(o_folder):
                    copy_file(d, f, o_folder)
                
        
if __name__ == "__main__":
    main(sys.argv[1])
            
            
            