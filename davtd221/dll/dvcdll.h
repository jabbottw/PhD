#ifndef _DVCDLL_H
#define _DVCDLL_H

/*

DaVince DLL subroutine definitions
Written by Dan Cogliano
Web Site: http://www.davince.com

*/
#ifndef _DVC_NO_NAMESPACE
namespace dvcdll {
#endif

#include "dvcexc.h"

extern "C" __declspec(dllimport) int createHandle();
extern "C" __declspec(dllimport) long setInfo(long handleid, const char *key,const char *value);
extern "C" __declspec(dllimport) long setParameter(long handleid, const char *key,const char *value);
extern "C" __declspec(dllimport) long writePdf(long handleid, const char *filename);
extern "C" __declspec(dllimport) long preparePdfBuffer(long handleid, long *pdfsize);
extern "C" __declspec(dllimport) long getPdfBuffer(long handleid, char *buff, long length);
extern "C" __declspec(dllimport) long rewindPdfBuffer(long handleid);
extern "C" __declspec(dllimport) long releaseHandle(long handleid);
extern "C" __declspec(dllimport) long convertTiffFile(long handleid, const char *filename, const char *aliasname);
extern "C" __declspec(dllimport) long convertTiffBuffer(long handleid, const char *filename, char *buff, long length);
extern "C" __declspec(dllimport) long convertFile(long handleid, const char *converter, const char *filename, const char *aliasname);
extern "C" __declspec(dllimport) long convertBuffer(long handleid, const char *converter, const char *filename, char *buff, long length);
extern "C" __declspec(dllimport) long getPageCount(long handleid, long *pagecount);
extern "C" __declspec(dllimport) long getInfoText(long handleid, char *key, char *buff, long size);
extern "C" __declspec(dllimport) long addPage(long handleid, long *pageid, float width, float height);
extern "C" __declspec(dllimport) long writePage(long handleid, long pageid, const char *buff, long length);
extern "C" __declspec(dllimport) long useFont(long handleid, long pageid, const char *fontname, const char *buff, long length);
extern "C" __declspec(dllimport) long getTextLength(long handleid, const char *fontname, const char *textstring, float pointsize, float *textlength);

#ifndef _DVC_NO_NAMESPACE
}
using namespace dvcdll;
#endif

#endif
