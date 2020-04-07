#!/bin/sh

value=''
builddir=`dirname $0`
cd $builddir
while read line 
do
#remove the last character in the line, it is not readable and not needed, like new line
    line=${line::-1}
    echo line: $line
    param=`echo $line|cut -d '=' -f1`
    if [[ $param = 'profile.home' ]] 
    then
	    value=`echo $line|cut -d '=' -f2`
	    echo was_profile:$value
	    break
    fi
done < was-config.properties
if [[ $value = '' ]]
then
	echo "Please configure the profile.home dir into the was.config.properties file and run again the script"
else
    ws_cmd=${value}/bin/ws_ant.sh
    ${ws_cmd} -buildfile $builddir/build.xml $@

fi

