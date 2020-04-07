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
	print "Sintaxe: installApplication.py filename, servers, clusternames, options "
else:
	commonPath = info.getCommonPath()
	execfile("%s/%s" % (commonPath, "wsadminlib.py"))
# 1.1.0	execfile('E:\jscripts\wsadminlib.py')
	filename, appname, servers, clusternames, contextroot, arglist = parseargs()
	enableDebugMessages()
	installApplication( filename, servers, clusternames, arglist )
	print "Contextroot: %s" %(contextroot)
	if contextroot <> None:
	   AdminApp.edit(appname, ['-CtxRootForWebMod', [[".*",".*",contextroot]]])
	save()
