# Authors: Sergio Stinchi

# Version        Description
# 1.0.0          Starting version
# Import 
import sys 
import java 
import time
from string import replace

commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))
  
# Variables 
scriptName = "CreateTopic.py" 
version = "1.0.0" 

skip = 'true'
# Data 
scopeName = ''             # mandatory [The name of the resource scope (i.e: Telematico, DogTelProNode01, ...) ]
                           #            Warning: if the scope is a server and its name is not unique on the cell 
                           #                     it must be used the form <Node>:<Server> 
TopicName = ''             # optional  [The Name of the Topic on Target BUS or MQ]
name = ''                  # mandatory [The name of the Topic]     
jndiName = ''              # mandatory [The jndi of the Topic]
targetClient = ''          # mandatory [Admitted values: JMS or MQ]
description = ''           # optional  [A description of the Topic]
deleteIfExist = 0          # 1 = delete the resource if exists
TopicSpace = ''            # mandatory [The Topic Space of the Topic]
DeliveryMode = ''          # optional  [Admitted values: Application, Persistent or Nonpersistent]

# JMS only
busName = ''               # mandatory [The bus of the Topic]

 
# Auxiliary functions 
def clearExit(text, status): 
   if len(text): print text 
   AdminConfig.reset() 
   print "%s done" % scriptName 
   sys.exit(status) 
   return 

#def checkIfTopicExist(scopeid, resourceName):
#   J2CAdminObjects = AdminTask.listSIBJMSTopics(scopeid)
#   if len(J2CAdminObjects) == 0: return None
#   for J2CAdminObject in J2CAdminObjects.splitlines():
#      name = AdminConfig.showAttribute(J2CAdminObject, 'name')
#      # print "name = %s - resourceName = %s  " % (name,resourceName) 
#      if name.find(resourceName) != -1:
#         return J2CAdminObject
#   return None   


# Command Line 
argc = len(sys.argv) 
if argc != 1: 
   print "Usage: %s <target data file>" % (scriptName) 
   sys.exit(-1) 
        
# Start 
print "%s V%s" % (scriptName, version) 
  

# Read target data file 
print "Read target data file ..." 
try: execfile(sys.argv[0]) 
except IOError, ioe: 
   print "ERROR: " + str(ioe) 
   sys.exit(-1) 
else: print "Read target data file done" 
  
# Check data read 
print "Check data read ..." 


if (targetClient == None) or (len(targetClient.strip()) == 0):
   print "ERROR: The variable targetClient is mandatory"
   print "%s done" % (scriptName)
   sys.exit(-1)
elif targetClient.strip() != 'JMS' and targetClient.strip() != 'MQ':
   print "ERROR: The variable targetClient has to be JMS or MQ"
   print "%s done" % (scriptName)
   sys.exit(-1)   
targetClient=targetClient.strip()   
     
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

if (TopicSpace == None) or len(TopicSpace.strip()) == 0:
   print "ERROR: The variable TopicSpace is mandatory"
   print "%s done" % (scriptName)
   sys.exit(-1)

if (DeliveryMode == None) or len(DeliveryMode.strip()) == 0:
   print "ERROR: The variable DeliveryMode is mandatory"
   print "%s done" % (scriptName)
   sys.exit(-1)
elif DeliveryMode.strip() != 'Application' and DeliveryMode.strip() != 'Persistent' and DeliveryMode.strip() != 'Nonpersistent':
   print "ERROR: The variable DeliveryMode has to be Application, Persistent or Nonpersistent"
   print "%s done" % (scriptName)
   sys.exit(-1)

if targetClient == 'JMS':
   if (busName == None) or (len(busName.strip()) == 0):
      print "ERROR: The variable busName is mandatory"
      print "%s done" % (scriptName)
      sys.exit(-1)

if deleteIfExist not in [0, 1]: 
   print "ERROR: The variable deleteIfExist can be 0 or 1" 
   print "%s done" % (scriptName) 
   sys.exit(-1) 
    
print "Check data read done" 
  
(scope, scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(scopeName)
# Create Topic 
if targetClient == 'MQ': 
   (resourceId , resourceName) = checkIfResourceExist(scopeid, name, "MQTopic")
   if resourceId != None: 
      print "Topic %s already exists" % name 
      if deleteIfExist == 1: 
         print "Delete existing Topic:",
         try: 
            AdminConfig.remove(resourceId) 
            print "OK" 
         except: 
            print "KO" 
            clearExit("Rollback and exit", -1)
   try: 
      print "Create MQ Topic %s:" % (name),
      useRFH2 = 'false' 
      command = "[-name %s -jndiName %s -topicName %s  -useRFH2 %s " % (name,jndiName,TopicName,useRFH2)
      if description!=None and len(description.strip()) != 0: command += " -description '%s' " % (description)
      command += "]"
      print "command = %s" % (command)
      print "AdminTask.createWMQTopic('%s', %s)" % (scopeid,command)
      AdminTask.createWMQTopic(scopeid, command)
      print "OK" 
   except: 
      print "KO" 
      type, value, traceback = sys.exc_info() 
      print "ERROR: %s (%s)" % (str(value), type) 
      clearExit("Rollback and exit", -1) 
   print "Create MQ Topic done" 

if targetClient == 'JMS': 
   if deleteIfExist == 1: skip = 'false'
   print "Check if SIB Jms Topic Exist ...... "
   (resourceId , resourceName) = checkIfResourceExist(scopeid, name, "J2CAdminObject")
   if resourceId != None: 
      if deleteIfExist == 1: 
         print "Topic %s already exists delete existing Topic." % name,
         try:
            AdminConfig.remove(resourceId)  
            print "OK" 
         except:
            print "KO"
            type, value, traceback = sys.exc_info() 
            print "ERROR: %s (%s)" % (str(value), type)
            clearExit("Rollback and exit", -1)
      else: 
            print "Topic %s already exists, skip creation " % name
   print "Check if Destination Exist ...... "
   out = checkIfDestinationExist(TopicSpace, busName) 
   if out != None: 
      if deleteIfExist == 1: 
         print "Destination %s already exists delete existing destination." % name,
         try: 
            AdminConfig.remove(out) 
            print "OK" 
         except:
            print "KO"
            type, value, traceback = sys.exc_info() 
            print "ERROR: %s (%s)" % (str(value), type)
            clearExit("Rollback and exit", -1)
      else: 
            print "Destination %s already exists, skip creation " % name

   # TO BE TESTED WITHOUT THE FOLLOWING LINE OF CODE
   #if AdminConfig.hasChanges() == 1:AdminConfig.save()
   if skip == 'false':
      print "Create Destination %s " % (TopicName),
      if description!=None and len(description.strip()) != 0: description = "-description '%s'" % (description)
      try:
         #print "AdminTask.createSIBDestination([-bus %s -name %s -type TopicSpace %s %s -reliability ASSURED_PERSISTENT ])" % (busName, TopicSpace, description)
         AdminTask.createSIBDestination("[-bus '%s' -name '%s' -type TopicSpace %s -reliability ASSURED_PERSISTENT ]" % (busName, TopicSpace, description))
         print "OK" 
         #if AdminConfig.hasChanges() == 1:AdminConfig.save()
      except:  
         print "KO"
         type, value, traceback = sys.exc_info() 
         print "ERROR: %s (%s)" % (str(value), type) 
         clearExit("Rollback and exit", -1)
      # Create Topic
      print "Create SIB Jms Topic ...."
      print "Create Topic %s " % (name),
      try:
         AdminTask.createSIBJMSTopic(scopeid, "[-name '%s' -jndiName %s -topicName '%s' %s -busName '%s' -deliveryMode %s -topicSpace '%s']" % (name, jndiName, TopicName, description, busName, DeliveryMode, TopicSpace)) 
         print "OK" 
         #if AdminConfig.hasChanges() == 1:AdminConfig.save()
      except:  
         print "KO"
         type, value, traceback = sys.exc_info() 
         print "ERROR: %s (%s)" % (str(value), type) 
         clearExit("Rollback and exit", -1)

      print "Create JMS Topic done" 
print "Save ..." 
syncEnv(AdminConfig.hasChanges())
 
print "%s V%s done" % (scriptName, version)
