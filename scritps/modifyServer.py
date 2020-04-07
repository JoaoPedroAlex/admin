#!/usr/bin/python
# Authors: Joao Pedro Alexandre

# Version   Changed by                          Description
#
# 1.1.0              
# 1.0.0                                                 Starting version

# Import
import sys
import java
from string import replace

commonPath = info.getCommonPath()
execfile("%s/%s" % (commonPath, "Utility.py"))

# Variables
scriptName = "modifyServer.py"
version = "1.0.0"

print "%s V%s" % (scriptName, version)

cellName, nodeName, serverName = getServerNode()
instPath = getInstPath()
# Read target data file
print "Read target data file ..."
#jvmFile = instPath + "/input/jvm.py"
jvmFile = sys.argv[0]
try: f = open(jvmFile, "r")
except IOError, ioe:
   print "ERROR: " + str(ioe)
   sys.exit(-1)
else: print "Open target data file done"
lines = f.readlines()
f.close()
# Check data read
print "Check data read ..."
for line in lines:
	array = line.split("=")
	var = array[0]
	value = array[1].rstrip()
	try:
		result = createJvmProperty(nodeName,serverName,var,value)
		print "jvm property %s created" % (AdminConfig.showAttribute(result,'name'))
		print "OK"
	except:
		print "KO"
		type, value, traceback = sys.exc_info()
		print "ERROR: %s (%s)" % (str(value), type)
		clearExit("Rollback and exit", -1)
print "Save ..."

save(AdminConfig.hasChanges())

# Done
print "%s V%s done" % (scriptName, version)


#setJvmProperty(nodeName,serverName,"genericJvmArguments","-Dcom.ibm.xml.xlxp.jaxb.opti.level=3 -Xverbosegclog:,10,40000 -Xdisableexplicitgc -Dsun.rmi.dgc.server.gcInterval=3600000 -Dsun.rmi.dgc.client.gcInterval=3600000")
#setJvmProperty(nodeName,serverName,"verboseModeGarbageCollection",'true')
#setJvmProperty(nodeName,serverName,"initialHeapSize",1024)
#setJvmProperty(nodeName,serverName,"maximumHeapSize",2048)

