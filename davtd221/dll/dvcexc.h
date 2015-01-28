#ifndef _DLLEXC_H
#define _DLLEXC_H

#include <string.h>

#ifndef string
        #define string std::string
#endif

class DLLException{
private:
        long _errorcode;
        string _errortext;

public:
        DLLException(long code, string val){_errorcode = code;_errortext = val;};
        long getErrorCode(){return _errorcode;};
        string setErrorText(string val){_errortext = val;};
        string getErrorText(){return _errortext;};
};

// this macro can be used with all DVCDLL functions except createHandle()
// for error processing via throw and catch
#define DLLERRORMESSAGE(handle,x) {int code = (x);\
	if(handle < 1) {string etext = "Invalid PDF handle passed to DVCLIB.DLL"; throw DLLException(-1,etext);} else if(code != 0){char buff[256]; getInfoText((handle),"ERROR",buff,255); string etext = buff; \
throw DLLException(code, etext);}}

#endif
