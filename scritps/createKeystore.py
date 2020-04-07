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
   print "Sintaxe: createKeyStore.py name scope(ex:cell1:node1:server1) description locationForkeystore password type(ex:CMSKS) "
else:
   print "Start creating keystore"
   commonPath = info.getCommonPath()
   execfile("%s/%s" % (commonPath, "wsadminlib.py"))
name = sys.argv[0]
scopearr = sys.argv[1].split(':')
desc = sys.argv[2]
location = sys.argv[3]
password = sys.argv[4]
type = sys.argv[5]
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
AdminTask.createKeyStore('[-keyStoreName '+name+' -scopeName '+scope+' -keyStoreDescription "'+desc+'" -keyStoreLocation '+location+' -keyStorePassword '+password+' -keyStorePasswordVerify '+password+' -keyStoreType '+type+' -keyStoreInitAtStartup false -keyStoreReadOnly false -keyStoreStashFile true ]')
save()