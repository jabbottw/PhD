import os
import imghdr

def get_ext(f):
    x = open(f, 'rb')
    if x.read(4) == '%PDF':
	    x.close()
            return 'pdf'
    elif imghdr.what(f) == 'tiff':
            return 'tiff'
    else:
	    return ''


main:

for i in files:
    old_file = i
    ext = get_ext(d + '\\' + i)
    if ext <> '':
        new_file = "%s%s%s" % (i, '.', ext)
    	shutil.copy(old_file, new_file)