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
scriptName = "setSecurity.py"
version = "1.0.0"

print "%s V%s" % (scriptName, version)
nodename = sys.argv[1]
cellName = sys.argv[0]
cert = sys.argv[2]
alias = sys.argv[3]
scope = "(cell):"+cellName+":(node):"+nodename
AdminTask.addSignerCertificate('[-keyStoreName NodeDefaultTrustStore -keyStoreScope '+scope+' -certificateFilePath '+cert+' -base64Encoded true -certificateAlias '+alias+']')
