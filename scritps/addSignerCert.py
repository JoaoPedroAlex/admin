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
scriptName = "addSignerCert.py"
version = "1.0.0"

print "%s V%s" % (scriptName, version)
keystore = sys.argv[0]
scopearr = sys.argv[1].split(':')
l = len(scopearr)
if l == 1:
  cellname = scopearr[0]
  scope = '(cell):'+cellname
elif l == 2:
  cellname = scopearr[0]
  nodename = scopearr[1] 	
  scope = '(cell):'+cellname+':(node):'+nodename
else:
   cellname = scopearr[0]
   nodename = scopearr[1]
   servername = scopearr[2]
   scope = '(cell):'+cellname+':(node):'+nodename+':(server):'+servername
cert = sys.argv[2]
alias = sys.argv[3]
if keystore == "NodeDefaultTrustStore":
  AdminTask.addSignerCertificate('[-keyStoreName NodeDefaultTrustStore -keyStoreScope '+scope+' -certificateFilePath '+cert+' -base64Encoded true -certificateAlias '+alias+']')
else:
  AdminTask.addSignerCertificate('[-keyStoreName '+keystore+' -keyStoreScope '+scope+' -certificateFilePath '+cert+' -base64Encoded true -certificateAlias '+alias+']')
save()