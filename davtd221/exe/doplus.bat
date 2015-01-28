@echo off
rem this batch file enables the plus settings in wdavince
copy %DTHOME%wdavincep.sav %DTHOME%wdavince.ini >nul:
echo "DaVince Tools Plus" settings have been enabled.
echo .
echo "DaVince Tools Plus" includes all the features of "DaVince Tools", plus the
echo file2pdf converter, DLL support and DLL sample programs. Enabling these
echo settings does not change your registration status, and registration
echo annotations may appear in PDF files if you have not registered either the
echo standard or plus version.
echo .
echo Restart wdavince to see the new settings.
