/*

  PDFCONV Program
  A sample application using the DaVince Tools DLL
  DaVince Web site: www.davince.com

  Convert TIFF, JPEG and text files to PDF
  Syntax: pdfconv file1 file2 ... filen

  This program creates a PDF file for each file specified on the
  command line. It places the PDF file in the same directory as
  the original file. This is a simplified version of file2pdf, which is part
  of "DaVince Tools Plus"

*/

#include <string>
#include <map>
#include <iostream>
#include <fstream>
#include <strstream>
#include <ctype.h>

#include "dvcdll.h"

using namespace std;

int main(int argc, char* argv[])
{
	long pdfhandle = 0;
    try
    {
        cout << "*** pdfconv: Convert a File to PDF (TIFF, JPEG and text)" << endl;
        cout << "*** DaVince Tools Plus Sample Application" << endl;
        cout << "*** Web Site: www.davince.com" << endl;
        cout << endl;
        if(argc < 2)
        {
                throw("Syntax: pdfconv file1 [file2] ... [filen]");
        }

        // set filetypes for each converter
		map < string, string, less<string> > ftype;

        // These are the file types we support.
        // left side: file extension, right side: converter to use
        ftype["tiff"] = "tiff";
        ftype["tif"] = "tiff";
        ftype["jpeg"] = "jpeg";
        ftype["jpg"] = "jpeg";
        ftype["text"] = "text";
        ftype["txt"] = "text";
        ftype["ini"] = "text";

        for(int i = 1; i < argc; i++)
        {
        // Initialize PDF handle with DLL
        pdfhandle = createHandle();
        DLLERRORMESSAGE(pdfhandle, setInfo(pdfhandle,"Title", "DaVince Tools Generated PDF File"));
        DLLERRORMESSAGE(pdfhandle, setParameter(pdfhandle, "Compression","true"));

        // use file extension to determine which converter to use
        int extpos = string(argv[i]).rfind(".");
        if(extpos < 0)
                throw string("a file extension is required to convert file ")
                        + string(argv[i]);
        string fileext = string(argv[i]).substr(extpos + 1);
        // convert extension to lower case, since "TIF" and ".tif" files
        // will be converted by the same converter
        for(int ii = 0; ii < fileext.length(); ii++)
                fileext.replace(ii,1,1,(char)tolower(fileext[ii]));

        cout << argv[i];
        cout.flush();
		if(ftype[fileext].length() == 0)
		{
			
			throw string("Unsupported file extension (\".") + fileext + string("\")");
		}
        DLLERRORMESSAGE(pdfhandle, convertFile(pdfhandle, ftype[ fileext ].c_str(), argv[i], ""));
        string pdffilename = string(argv[i]).substr(0,extpos) + string(".pdf");
        cout << " writing " << pdffilename;
        cout.flush();
        DLLERRORMESSAGE(pdfhandle, writePdf(pdfhandle, pdffilename.c_str()));
        cout << endl;

        releaseHandle(pdfhandle);
        }
    }
    catch (DLLException &e)
    {
        cerr << "*** pdfconv DLL error: " <<  e.getErrorText() << endl;
		releaseHandle(pdfhandle);
        return 1;
    }
    catch (string &e)
    {
        cerr << "*** " << e << endl;
		releaseHandle(pdfhandle);
		return 1;
    }
    catch (...)
    {
        cerr << "*** pdfconv application error" << endl;
		releaseHandle(pdfhandle);
        return 1;
    }
        return 0;
}

