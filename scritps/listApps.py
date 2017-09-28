# Authors: Joao Alexandre

# Version        Description
#
# 1.0.0          Starting version
# Import 
import sys 
import java 
import time

commonPath = info.getCommonPath()
infoPath = info.getInfoPath()
execfile("%s/%s" % (commonPath, "wsadminlib.py"))

scriptName = "listApps.py"
version = "1.0.0"

enableDebugMessages()
	#sop("installApp:","contextroot=%s" % contextroot)
listApplications()
	
