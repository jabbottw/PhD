@echo off
rem this batch file disables the plus settings for wdavince
copy %DTHOME%wdavince.sav %DTHOME%wdavince.ini >nul:
echo DaVince Tools Plus settings have been disabled.
echo .
echo This does not change your registration status.
echo .
echo Restart wdavince to see the new settings.
