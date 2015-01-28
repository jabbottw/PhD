#ifndef _DLLEXC_H
#define _DLLEXC_H

#include <string>

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
//#define DLLERRORCHECK(x) {int code = (x); if(code != 0) throw DLLException(code,#x);}
#define DLLERRORMESSAGE(handle,x) {int code = (x); if(code != 0){char buff[256]; int code2 = getInfoText((handle),"ERROR",buff,255); string etext = buff; \
throw DLLException(code, etext);}}

#endif
