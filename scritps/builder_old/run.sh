#!/bin/ksh

value=''
builddir=`dirname $0`
cd $builddir
while read line 
do
	param=`echo $line|cut -d '=' -f1`
	if [[ $param = 'DeploymentManagerBin' ]] 
	then
		value=`echo $line|cut -d '=' -f2`
		break
	fi
done < Resources.properties
if [[ $value = '' ]]
then
	echo "Please configure the Deployment Manager bin into the Resources.properties file and run again the script"
else
	$value/ws_ant.sh -buildfile $builddir/build.xml $@

fi

