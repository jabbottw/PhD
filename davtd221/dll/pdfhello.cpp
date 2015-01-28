/*

  PDFHELLO Program
  A sample application using the DaVince Tools DLL
  DaVince Web site: www.davince.com

  Create a single page PDF file with the words "Hello World"
  Syntax: pdfhello

*/

#include <string>
#include <iostream>
#include <fstream>
#include <strstream>
#include <ctype.h>

#include "dvcdll.h"

using namespace std;

int main(int argc, char* argv[])
{
    long pdfhandle = 0;
    string filename = "pdfhello.pdf";

    try
    {
        // initialize PDF
        pdfhandle = createHandle();
        DLLERRORMESSAGE(pdfhandle, setInfo(pdfhandle,"Title", "Hello World"));
        DLLERRORMESSAGE(pdfhandle, setParameter(pdfhandle, "Compression","true"));

        // create page
                long pagehandle;
        DLLERRORMESSAGE(pdfhandle, addPage(pdfhandle, &pagehandle, 8.5*72, 11.0*72));

        // create page stream
        // define a buffer size that will be big enough to store our page stream
        #define BUFFSIZE (1024*10)
        char buff[BUFFSIZE];
        strstream spage(buff, BUFFSIZE);

        //select font to use
        char shortname[20];
        DLLERRORMESSAGE(pdfhandle, useFont(pdfhandle, pagehandle, "Helvetica", shortname, 20));

        // determine text length of "Hello World" in order to center it horizontally on the page
        float textlength;
        DLLERRORMESSAGE(pdfhandle, getTextLength(pdfhandle, "Helvetica", "Hello World", 72, &textlength));
        float horizontalpos = (8.5*72 - textlength)/2;

        // write page description to stream
        spage << "q ";
        spage << "BT ";
        spage << "/" << shortname << " 72 Tf ";

        spage << horizontalpos << " 576 Td (Hello World) Tj ";
        spage << "ET ";
        spage << "Q" << endl;
        long pagesize = spage.tellp();
        DLLERRORMESSAGE(pdfhandle, writePage(pdfhandle, pagehandle, buff, pagesize));
        cout << "writing to " << filename << endl;
        DLLERRORMESSAGE(pdfhandle, writePdf(pdfhandle,filename.c_str()));
        releaseHandle(pdfhandle);
    }
    catch (DLLException &e)
    {
        cerr << "*** pdfhello DLL error: " <<  e.getErrorText() << endl;
        releaseHandle(pdfhandle);
        return 1;
    }
    catch (...)
    {
        cerr << "*** pdfhello application error" << endl;
        releaseHandle(pdfhandle);
        return 1;
    }
    return 0;
}
 
