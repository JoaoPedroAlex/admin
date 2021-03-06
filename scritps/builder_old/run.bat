@echo off
set mydir=%~dp0
call "%mydir%install.properties.bat"
IF EXIST "%eclipseJreLocation%" goto setEclipseJdk

:myCmd
set WS_ANT_HOME=%WAS_PROFILE_DIR%

REM Depending on DOS cmd prompt code page in use, you may have to set file.encoding option to see correct output.
REM Run chcp command in a DOS cmd prompt an search for the corresponding java encoding canonical name under
REM http://docs.oracle.com/javase/7/docs/technotes/guides/intl/encoding.doc.html
REM set ANT_OPTS=-Dfile.encoding=Cp850
REM The next lines handle the most common cases
for /F "tokens=2 delims=:" %%A in ('chcp') do set cp_with_space=%%A
SET cp=%cp_with_space: =%
set ANT_OPTS=-Dfile.encoding=Cp%cp%

call "%WS_ANT_HOME%\bin\ws_ant.bat" -buildfile "%mydir%\build.xml" %*
pause
goto endScript

:setEclipseJdk
set JAVA_HOME=%eclipseJreLocation%
goto myCmd

:endScript