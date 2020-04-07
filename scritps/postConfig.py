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
scriptName = "postConfig.py"
version = "1.0.0"

print "%s V%s" % (scriptName, version)
nodename = sys.argv[0]
servername = sys.argv[1]
appName = sys.argv[2]
print "%s - %s" % (nodename, servername)
id = modifyUrlRewriting(nodename,servername,"true")
print "%s - id: %s" % (scriptName, id)
setClassloaderToParentLast(appName)
AdminApp.edit(appName, '[-MapResRefToEJB [[ imex-web "" imexgw.war,WEB-INF/web.xml imexGatewayURL java.net.URL url/imxprg "" "" "" ][ imex-web "" imexgw.war,WEB-INF/web.xml imexCICSini javax.resource.cci.ConnectionFactory eis/imxprd "" "" "" ][ imex-web "" imexgw.war,WEB-INF/web.xml imexCICS javax.resource.cci.ConnectionFactory eis/imxprd "" "" "" ][ imex-web "" imexgw.war,WEB-INF/web.xml imexDB javax.sql.DataSource jdbc/imxprd "" "" "" ]]]')
save()