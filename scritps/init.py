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
scriptName = "init.py"
version = "1.0.0"
cellName = ""
nodeName = ""
serverName = ""

print "%s V%s" % (scriptName, version)
server = AdminConfig.list('Server')
#'server1(cells/PSCell1/nodes/Node1/servers/server1|server.xml#Server_1183122130078)'
array = server.split("(")
serverName = array[0]
array = array[1].split("/")
cellName = array[1]
nodeName = array[3]
print "%s %s %s" % (cellName, nodeName, serverName)
instPath = getInstPath()
wasConfig = instPath + "/was-config.properties"
f = open(wasConfig, "a")
f.write("\ncellName=%s\n" % cellName)
f.write("nodeName=%s\n" % nodeName)
f.write("serverName=%s" % serverName)
f.close()
print "%s ended" % (scriptName)

