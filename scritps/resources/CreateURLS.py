# Authors: Sergio Stinchi

# Version        Description
# 1.2.0          Changed check for resources
# 1.1.0          Add Function checkScopeName()
# 1.0.0          Starting version

# Import
import sys
import java
from string import replace

commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))

# Variables
scriptName = "CreateURLS.py"
version = "1.2.0"


print "%s V%s" % (scriptName, version)

# Auxiliary functions
def clearExit(text, status):
   if len(text): print text
   AdminConfig.reset()
   print "%s done" % scriptName
   sys.exit(status)
   return

#def checkIfResourceExist(scopeid, resourceName, typeObject):
#   try:
#      url = AdminConfig.list(typeObject,scopeid) 
#      #print "URL=%s" % (url)
#      if len(url) == 0: return None
#      if url.find(resourceName + '(') != -1:
#         beg = url.find(resourceName + '(')
#         end = url.find(')', beg) + 1
#         return url[beg:end]
#   except:
#      print "KO"
#      type, value, traceback = sys.exc_info()
#      print "ERROR: %s (%s)" % (str(value), type)
#      clearExit("Rollback and exit", -1)

# Command Line
argc = len(sys.argv)
if argc != 1:
   print "Usage: %s <target data file>" % (scriptName)
   sys.exit(-1)
        
# Start
print "%s V%s" % (scriptName, version)

# Data
scopeName = ''               # mandatory [The name of the resource scope (i.e: Telematico, DogTelProNode01, ...)]
                             #            Warning: if the scope is a server and its name is not unique on the cell
                             #                     it must be used the form <Node>:<Server>
name = ''                    # mandatory [The name of the resource]     
jndiName = ''                # mandatory [The jndi of the resource]
providerName=''              # mandatory [Specifies the URL provider name for the URL configuration.]
spec=''                      # mandatory [Specifies the string from which to form a URL.]
deleteIfExist=0


# Read target data file
print "Read target data file ..."
try: execfile(sys.argv[0])
except IOError, ioe:
   print "ERROR: " + str(ioe)
   sys.exit(-1)
else: print "Read target data file done"

# Check data read
print "Check data read ..."

if (scopeName == None) or (len(scopeName.strip()) == 0):
   print "ERROR: The variable scopeName is mandatory"
   print "%s done" % (scriptName)
   sys.exit(-1)
   
if (name == None) or (len(name.strip()) == 0):
   print "ERROR: The variable name is mandatory"
   print "%s done" % (scriptName)
   sys.exit(-1)

if (jndiName == None) or len(jndiName.strip()) == 0:
   print "ERROR: The variable jndiName is mandatory"
   print "%s done" % (scriptName)
   sys.exit(-1)

if (providerName == None) or (len(providerName.strip()) == 0):
   print "ERROR: The variable providerName is mandatory"
   print "%s done" % (scriptName)
   sys.exit(-1)
   
if (spec == None) or (len(spec.strip()) == 0):
   print "ERROR: The variable spec is mandatory"
   print "%s done" % (scriptName)
   sys.exit(-1)

if deleteIfExist not in [0, 1]:
   print "ERROR: The variable deleteIfExist can be 0 or 1"
   print "%s done" % (scriptName)
   sys.exit(-1)
   
print "Check data read done"

# set default values

# Check scopeName ...
print "Check scope %s ..." % (scopeName)
(scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(scopeName)   


# Create URL
print "Create URL ... %s" % (name)
#out = checkIfResourceExist(scopeid, name, 'URL')
#print "out= %s" % (out)
#if out!=None:
(resourceId , resourceName) = checkIfResourceExist(scopeid, name, "URL")
if resourceId != None: 
   print "URL %s already exists " % (name) 
   if deleteIfExist == 1:
      print "Delete existing URL:",
      try: 
#         AdminConfig.remove(out)
         AdminConfig.remove(resourceId)
         print "OK"
      except: clearExit("KO\nRollback and exit", -1) 
   else: clearExit("", 0)   
print "Create %s:" % (name)

try:
   print "Create URL %s " % (name),
   name = ['name', name]
   spec = ['spec', spec]
   jndiName = ['jndiName', jndiName]
   UrlProviderList = AdminConfig.list('URLProvider',scopeid)
   providerID=UrlProviderList.splitlines()[0]
   providerName=AdminConfig.showAttribute(providerID,'name')
   urlAttrs = [name, jndiName, spec]
   ulrId = AdminConfig.create('URL', providerID, urlAttrs)         
   print "URL %s created" % (AdminConfig.showAttribute(ulrId,'name'))
   print "OK"
except:
   print "KO"
   type, value, traceback = sys.exc_info()
   print "ERROR: %s (%s)" % (str(value), type)
   clearExit("Rollback and exit", -1)
print "Save ..."

save(AdminConfig.hasChanges())
# Done
print "%s V%s done" % (scriptName, version)
