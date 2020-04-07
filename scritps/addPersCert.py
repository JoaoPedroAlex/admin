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
scriptName = "addPersCert.py"
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
passwd = sys.argv[4]
AdminTask.importCertificate('[-keyFilePath '+cert+' -keyFilePassword '+passwd+' -keyFileType PKCS12 -certificateAliasFromKeyFile '+alias+' -certificateAlias '+alias+' -keyStoreName '+keystore+' -keyStoreScope '+scope+' ]')
save()