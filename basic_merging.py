
from PyPDF2 import PdfFileMerger
from os.path import join
import re
import os
print "start merge" 
rootdir = r'H:\ColoradoUpdate\rawFiles'
outdir = r'H:\ColoradoUpdate\updates'

            
def tryint(s):
    try:
        return int(s)
    except:
        return s
    
def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)

# Main function to merge all pdf files
outputReport = []
for subdir, dirs, files in os.walk(rootdir):
        merger = PdfFileMerger()
        if subdir[-4:] == "0000":
            outFileName = subdir[-14:]
            output = join(outdir, outFileName + '_PhD_WellFile.pdf')
            if not os.path.exists(output):
                print "Folder: " + outFileName
                fileArray = []
                for f in files:
                    fileArray.append(join(subdir,f))
                sort_nicely(fileArray)
                for f in fileArray:
                    try:
                        print "Merging: " + join(subdir, f)
                        merger.append(open(join(subdir, f), "rb"))            
                    except:
                        print "Couldn't add file: " + f
                print "Writing Output file: " + output
                try:
                    merger.write(output)
                except:
                    outputReport.append("Couldn't create file: " + subdir[-14:])
for i in outputReport:
    print i
        
        
''' Some sample notes on the pdf merge process
path = r'C:\f'

input1 = open(path + "\\a.pdf", "rb")
input2 = open(path + "\\b.pdf", "rb")
input3 = open(path + "\\c.pdf", "rb")

# add the first 3 pages of input1 document to output
merger.append(input1)

# insert the first page of input2 into the output beginning after the second page
merger.append(input2)

# append entire input3 document to the end of the output document
merger.append(input3)

# Write to an output PDF document
output = open(path + "\document-output2.pdf", "wb")
merger.write(output)
'''