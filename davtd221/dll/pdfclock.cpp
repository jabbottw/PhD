/*

  PDFCLOCK PROGRAM
  A sample application using the DaVince Tools DLL
  DaVince Web Site: http://www.davince.com

  This program creates a PDF file containing a clock with the current time.
  Can be used either on a command line or as a CGI (web) application.

  Command line syntax
  pdfclock [filename]

  filename - PDF file to use to create the clock image.

  if a filename is not specified on the command line, "pdfclock.pdf" is used.
*/

#include <string>
#include <iostream>
#include <fstream>
#include <strstream>
#include <math.h>
#include <time.h>
#include <io.h>

#include "dvcdll.h"

// all numeric defines are in points
#define CLOCKSIZE 400
#define RADIUS 190
#define MINUTEHAND 190
#define HOURHAND 140
#define HANDWIDTH HOURHAND/10.
#define TEXTWIDTH 190
#define CLOCKTITLE "DaVince Tools"
// Mathemetical PI constant
#define PI 3.14159265

// use PDFFLOAT to round small floating point values to zero, otherwise, small
// values will print in scientific notation, which PDF does not recognize.
#define PDFFLOAT(x)(((double)((int)((x)*1000.)))/1000.)

using namespace std;


// draw clock hands or clock hand shadows
void drawHands(ostream &spage, tm *timenow, bool shadow)
{
        // calculate angles used for clock hands
        double hourangle = (12. - ((timenow->tm_hour % 12) + timenow->tm_min / 60.)) / 12.
            * 2. * PI + PI / 2.;
        double minuteangle = (60. - (timenow->tm_min / 60.))
            * 2. * PI + PI / 2.;

        // draw clock

        spage << "q" << endl;
    	if(shadow)
		{
			spage << ".9 .9 .9 rg " << endl;
		}
		else
		{
			spage << "0 0 0 rg .5 .5 .5 RG 1 w" << endl;
		}
        // hour hand
        spage << PDFFLOAT(cos(hourangle)) << " " << PDFFLOAT(sin(hourangle)) << " " <<
            0. - PDFFLOAT(sin(hourangle)) << " " << PDFFLOAT(cos(hourangle));
		if(shadow)
			spage << " 10 -10 cm " << endl;
		else
			spage << " 0 0 cm " << endl;
        spage << HOURHAND << " 0 m " << (0 - HANDWIDTH) << " "
            << HANDWIDTH << " l " << (0 - HANDWIDTH) << " "
            << (0 - HANDWIDTH) << " l ";
		if (shadow)
			spage << "h f" << endl;
		else
			spage << "b" << endl;
        spage << "Q" << endl;

        // minute hand
        spage << "q" << endl;
    	if(shadow)
		{
			spage << ".9 .9 .9 rg " << endl;
		}
		else
		{
			spage << "0 0 0 rg .5 .5 .5 RG 1 w" << endl;
		}
        spage << PDFFLOAT(cos(minuteangle)) << " " << PDFFLOAT(sin(minuteangle)) << " " <<
            0. - PDFFLOAT(sin(minuteangle)) << " " << PDFFLOAT(cos(minuteangle));
		if(shadow)
			spage << " 10 -10 cm " << endl;
		else
			spage << " 0 0 cm " << endl;
        spage << MINUTEHAND << " 0 m " << (0 - HANDWIDTH) << " "
            << HANDWIDTH << " l " << (0 - HANDWIDTH) << " "
            << (0 - HANDWIDTH) << " l ";
		if (shadow)
			spage << "h f" << endl;
		else
			spage << "b" << endl;
        spage << "Q" << endl;

}

int main(int argc, char **argv)
{
    long pdfhandle = 0;
    try{
        time_t secnow;
        tm *timenow;
        string filename = "pdfclock.pdf";
        if(argc > 1)
                filename = argv[1];

        time(&secnow);
        timenow = localtime(&secnow);

        // Initialize PDF handle with DLL
        pdfhandle = createHandle();
        DLLERRORMESSAGE(pdfhandle, setInfo(pdfhandle,"Title", "DaVince Tools Clock Demo"));
        DLLERRORMESSAGE(pdfhandle, setParameter(pdfhandle, "OpenAction","Fit"));
        DLLERRORMESSAGE(pdfhandle, setParameter(pdfhandle, "Compression","true"));
        long pagehandle;
        DLLERRORMESSAGE(pdfhandle, addPage(pdfhandle, &pagehandle, (float)CLOCKSIZE, (float)CLOCKSIZE));

        // create page stream
        // define a buffer size that will be big enough to store our page stream
        #define BUFFSIZE (1024*20)
        char buff[BUFFSIZE];
        strstream spage(buff, BUFFSIZE);
		spage << "q ";
		spage << "1 0 0 1 " << CLOCKSIZE/2 << " " << CLOCKSIZE/2 << " cm " << endl;
 		drawHands(spage, timenow, true);

        // draw clock title
        // the text length is fixed, so we need to adjust the point size to fit
        // in the given length

        char shortname[20];
        DLLERRORMESSAGE(pdfhandle, useFont(pdfhandle, pagehandle, "Helvetica-Oblique", shortname, 20));
        float textlength;
        DLLERRORMESSAGE(pdfhandle, getTextLength(pdfhandle, "Helvetica-Oblique", CLOCKTITLE, 1., &textlength));
        float fontsize = TEXTWIDTH / textlength;
        spage << "BT" << endl;
        spage << "/" << shortname << " " <<
            fontsize << " Tf " << endl;
        float startx = 0 - TEXTWIDTH / 2.;
        float starty = 0 - CLOCKSIZE / 4.;
        spage << startx
            << " " << starty << " Td" << endl;
        spage << "(" << CLOCKTITLE << ")" << " Tj" << endl;
        spage << "ET" << endl;

        // draw today's date

        // draw rectangle where date will go

        char numbuff[10];
        strstream strstr(numbuff,10);
        strstr << timenow->tm_mday << ends;
        string numstr(numbuff);

        DLLERRORMESSAGE(pdfhandle, useFont(pdfhandle, pagehandle, "Helvetica", shortname, 20));
        DLLERRORMESSAGE(pdfhandle, getTextLength(pdfhandle, "Helvetica", numbuff, 1., &textlength));
        float rheight = CLOCKSIZE / 20.;
        float rwidth;
        DLLERRORMESSAGE(pdfhandle, getTextLength(pdfhandle, "Helvetica", "00", 1., &rwidth));
		rwidth = rheight * rwidth;
        spage << "q ";
        //spage << "1 0 0 1 " << CLOCKSIZE/2 << " " << CLOCKSIZE/2 << " cm " << endl;
        spage << "2 w " << (RADIUS - 10 - rwidth - 5 - 2) << " " << (0 - rheight / 2. - 2) <<
        " " << rwidth + 4 << " " << rheight + 4 << " re S Q" << endl;

        // put the date in the box
        fontsize = rheight;
        startx = (RADIUS - 10 - textlength * rheight - 5);
        starty = 0 - rheight / 2 + (0.2 * textlength) * rheight;
        spage << "q" << endl;
        //spage << "1 0 0 1 " << CLOCKSIZE/2 << " " << CLOCKSIZE/2 << " cm " << endl;
        spage << "BT " << "/" << shortname << " " <<
            fontsize << " Tf " << endl;
        spage << startx
            << " " << starty << " Td" << endl;
        spage << "(" << numstr << ")" << " Tj" << endl;
        spage << "ET Q" << endl;

        // draw 1 second tick marks
        spage << "q ";
        spage << "5 w ";
        spage << "q ";
        for(int incr = 0; incr < 60; incr++)
        {
            if((incr % 5 ) == 0)
                spage << RADIUS << " 0 m " << (RADIUS - 10) << " 0 l S" << endl;
            else
                spage << RADIUS << " 0 m " << (RADIUS - 5) << " 0 l S" << endl;
            double angle = 2*PI / 60;
            spage << cos(angle) << " " << sin(angle) << " " <<
                0 - sin(angle) << " " << cos(angle) << " 0 0 cm " << endl;
        }
        spage << "Q " << endl;

        // draw clock hands

        drawHands(spage, timenow, false);

        spage << "Q" << endl;
        long pagesize = spage.tellp();
        DLLERRORMESSAGE(pdfhandle, writePage(pdfhandle, pagehandle, buff, pagesize));

        // PDF is complete, now write to output stream
        // write to cout if running as a CGI program, otherwise write to a file

        // is this running as a CGI program?
        if(getenv("GATEWAY_INTERFACE") != 0)
        {
            // it is, print HTTP header info and PDF output to cout
            long pdfsize;
            DLLERRORMESSAGE(pdfhandle, preparePdfBuffer(pdfhandle,&pdfsize));
            // set cout to binary mode to prevent pdf from getting corrupted
            cout.flush();
            setmode(1,O_BINARY);
            cout << "Content-Type: application/pdf" << endl;
            cout << "Content-Length: " << pdfsize << endl << endl;
            char *pdfbuff = new char[pdfsize];
            // char buff[BUFFSIZE];
            DLLERRORMESSAGE(pdfhandle, getPdfBuffer(pdfhandle, pdfbuff, pdfsize));
            cout.write(pdfbuff, pdfsize);
            cout.flush();
            delete [] pdfbuff;
        }
        else
        {
                cout << "writing to " << filename << endl;
                DLLERRORMESSAGE(pdfhandle, writePdf(pdfhandle,filename.c_str()));
        }
        releaseHandle(pdfhandle);

    }
    catch (DLLException &e)
    {
        cerr << "*** pdfclock DLL error: " <<  e.getErrorText() << endl;
        releaseHandle(pdfhandle);
        return 1;
    }
    catch (...)
    {
        cerr << "*** pdfclock application error" << endl;
        releaseHandle(pdfhandle);
        return 1;
    }
    return 0;
}

