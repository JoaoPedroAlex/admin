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
execfile("%s/%s" % (commonPath, "wsadminlib.py"))

# Variables
scriptName = "createWebserver.py"
version = "1.0.0"

print "%s V%s" % (scriptName, version)
nodename = sys.argv[0]
servername = sys.argv[1]
webPort = sys.argv[2]
webInstallRoot = sys.argv[3]
pluginInstallRoot = sys.argv[4]
configurationFile = sys.argv[5]
webAppMapping = sys.argv[6]
adminPort = sys.argv[7]
adminUserID = sys.argv[8]
adminPasswd = sys.argv[9]
createWebserver(servername, nodename, webPort, webInstallRoot, pluginInstallRoot,configurationFile, webAppMapping, adminPort, adminUserID, adminPasswd)
# AdminTask.createWebServerByHostName('[-webserverName webserver1 -templateName IHS -webPort 80 -serviceName IBMHTTPServerV8.5 -webInstallRoot "C:\IBM\HTTPServer" -webProtocol HTTP -configurationFile  -errorLogfile  -accessLogfile  -pluginInstallRoot c:\IBM\WebSphere\Plugins -webAppMapping ALL -hostName ibmbpm-rpa -platform windows -adminPort 8008 -adminUserID admin -adminPasswd ******** -adminProtocol HTTP]')
save()