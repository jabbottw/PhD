"""
/***************************************************************************
Name                 : PHD Utility methods
Description          : Tool set designed to download data over the internet
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
            
def tiff2pdf(src_file):
    #exe =  join(os.path.dirname(os.path.abspath(__file__)), r'davtd221\exe\tiff2pdf.exe')
    exe = r'C:\Users\Julian\.qgis2\python\plugins\davtd221\exe\tiff2pdf.exe'
    os.system('%s -1 %s' % (exe, src_file))
    os.remove(src_file)
    
    
def rm_empty_dirs(root):
    sub_dirs = listdir(root)
    for f in sub_dirs:
        folder = join(root, f)
        if isdir(folder):
            if os.listdir(folder) == []:
                try:
                    os.rmdir(folder)
                except:
                    pass
                             
def get_ext(f):
    x = open(f, 'rb')
    if x.read(4) == '%PDF':
        x.close()
        return 'pdf'
    elif imghdr.what(f) == 'tiff':
        return 'tiff'
    else:
        return ''

def set_file_ext(old_file, ext):
    new_file = old_file + '.' + ext
    shutil.copy(old_file, new_file)
    os.remove(old_file)

def makeFolder(outputFolder):
    """ Make a folder using the outputFolder path variable. If the outputFolder exist, this method will overwrite the existing directory """
    try:
        if not os.path.exists(outputFolder):
            os.makedirs(outputFolder)
        else:
            shutil.rmtree(outputFolder)
            os.makedirs(outputFolder)
        return True
    except:
        return False
        
def cleanCO_API(api):
    """ Clean the default COGCC API provided by the state. This should be in the form of 05-xxx-xxxxx
        This function will remove the dashes and tack on the last four zeros. 
        Split the provided api into a list using the dashes """
    apiSplit = api.split("-")
    # Create the final variable to be returned
    apiConcat = ""
    # Concate the list into a single variable
    for i in apiSplit:
        apiConcat = "%s%s" % (apiConcat, i)
    # Add the final four zeros if len of the current api = 10
    if (len(apiConcat) == 10):
        apiConcat = "%s%s" % (apiConcat, "0000")
    if (len(apiConcat) == 12):
        apiConcat = "%s%s" % (apiConcat, "00")
    return apiConcat


# utility methods
def find_substring(key_words, word_list):
    ''' search for a key word within the provided search string
        Handles case sensitivity by converting all words to a lower case representation
        method returns a boolean true false value'''
    # split search string into it's indavidual words
    key_word_list = key_words.split()
    for kw in key_word_list:
        for word in word_list:
            if kw.lower() == word.lower():
                return True
        return False