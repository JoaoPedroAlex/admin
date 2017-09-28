#!/usr/bin/python
# Authors: Joao Pedro Alexandre

# Version        Description
# 1.3.0        
# 1.2.0         
# 1.1.0          Some improvements to avoid static directories references in the script
# 1.0.0          Starting version

# Import
import getopt, sys
arglen = len(sys.argv)
if arglen < 1:
  print "Sintaxe: setClassloaderToParentLast.py appname"
else:
# 1.1.0  execfile('/opt/IBM/was/jscripts/wsadminlib.py')
	commonPath = info.getCommonPath()
	execfile("%s/%s" % (commonPath, "wsadminlib.py"))
	enableDebugMessages()
	appname = sys.argv[0]
	setClassloaderToParentLast(appname)
	save()