# Authors: Sergio Stinchi

# 1.0.2          Removing mandatory for Queue Manager and changed check for resources
# 1.0.1          Patching scope definition
# 1.0.0          Starting version

import sys
import java
from string import replace

# Variables
scriptName = "createConnectionFactory.py"
version = "1.0.2"


commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))

# Auxiliary functions
def clearExit(text, status):
   if len(text): print text
   AdminConfig.reset()
   print "%s done" % scriptName
   sys.exit(status)
   return


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
name = ''                    # mandatory [The name of the Connection Factory]     
jndiName = ''                # mandatory [The jndi of the Connection Factory]
targetClient = ''            # mandatory [Admitted values: JMS or MQ]
authenticationAlias = ''           # optional
xaRecoveryAuthAlias=''       # optional
description = ''             # optional  [A description of the Connection Factory]
provider=''                  # optional  [Read only]
deleteIfExist = 0            # 1 = delete the resource if exists

# JMS only
Type=''                      # optional  [Admitted values: queue or topic. If empty creates a generic Connection factory]
JMSbusName = ''              # mandatory [The bus of the Connection Factory]

# MQ only 
typeConnectionFactory=''     # mandatory [Admitted values: MQConnectionFactory or MQQueueConnectionFactory  
                             #            READ ONLY for JMS can have the following values: ConnectionFactory, QueueConnectionFactory or TopicConnectionFactory]
MQqueueManager =''           # optional  [The Queue Manager that hosts the Connection Factory] 
MQhostName =''               # optional  [hostname of the Queue Manager. If empty local host used]
MQport=''                    # optional  [port of the Queue Manager]
MQchannel=''                 # optional  [channel of the Queue Manager]
MQtransportType =''          # optional  [The way in which a connection is established to WebSphere MQ for this activation specification.
                             #            Admitted values: BINDINGS, BINDINGS_THEN_CLIENT or CLIENT. BINDINGS_THEN_CLIENT is the default value.]
		 
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

if (targetClient == None) or (len(targetClient.strip()) == 0):
   print "ERROR: The variable targetClient is mandatory"
   print "%s done" % (scriptName)
   sys.exit(-1)
elif targetClient.strip() != 'JMS' and targetClient.strip() != 'MQ':
   print "ERROR: The variable targetClient has to be JMS or MQ"
   print "%s done" % (scriptName)
   sys.exit(-1)   
targetClient=targetClient.strip()   
   
if targetClient == 'JMS':
   if (JMSbusName == None) or (len(JMSbusName.strip()) == 0):
      print "ERROR: The variable JMSbusName is mandatory"
      print "%s done" % (scriptName)
      sys.exit(-1)
   if (Type != None) and (len(Type.strip()) != 0):
      if Type.strip() != 'queue' and Type.strip() != 'topic':
         print "WARNING: The variable Type has to be queue or topic. Creating generic Connection Factory."
         Type = ''
elif targetClient == 'MQ':
   if len(MQchannel) > 20:
      print "ERROR: The variable MQchannel cannot be longer of 20 characters"
      print "%s done" % (scriptName)
      sys.exit(-1)
      
   if (MQport != None) and len(MQport.strip()) != 0 :
      if MQport.strip().isdigit():
         if int(MQport) <=0:
            print "WARNING: The variable MQport has to be > 0. Using default 1414"
            MQport = '1414'
      else:
         print "WARNING: The variable MQport has to be numeric. Using default 1414"
         MQport = '1414'
   
   if (typeConnectionFactory != None) and len(typeConnectionFactory.strip()) != 0 :
      if typeConnectionFactory == 'MQConnectionFactory':
         Type='CF'
      elif typeConnectionFactory == 'MQQueueConnectionFactory':
         Type='QCF'
      else:
         print "WARNING: The variable typeConnectionFactory has to be MQConnectionFactory or MQQueueConnectionFactory. Creating generic MQ Connection Factory."
         Type=''

   if (MQtransportType != None) and len(MQtransportType.strip()) != 0 :
      if MQtransportType.strip() not in ['BINDINGS', 'BINDINGS_THEN_CLIENT', 'CLIENT']:
         print "ERROR: The variable MQtransportType could be only ['BINDINGS', 'BINDINGS_THEN_CLIENT', 'CLIENT']"
         print "%s done" % (scriptName)
         sys.exit(-1)


if deleteIfExist not in [0, 1]:
   print "ERROR: The variable deleteIfExist can be 0 or 1"
   print "%s done" % (scriptName)
   sys.exit(-1)
   
print "Check data read done"
# Check scopeName ...
print "Check scope %s ..." % (scopeName)

(scope, scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(scopeName)

# Create Connection Factory
print "Create Connection Factory ..."
#out = checkIfResourceExist(scopeid, name ,'ConnectionFactory')
#if out != None:
(resourceId , resourceName) = checkIfResourceExist(scopeid, name, "ConnectionFactory")
if resourceId != None: 
   print "Connection Factory %s already exists" % name
   if deleteIfExist == 1:
      print "Delete existing Connection Factory:",
      try: 
#         AdminConfig.remove(out)
         AdminConfig.remove(resourceId)
         print "OK"
      except: clearExit("KO\nRollback and exit", -1)
   else: clearExit("", 0)   

if Type!=None and len(Type.strip()) != 0: Type = '-type %s' % (Type)
if description!=None and len(description.strip()) != 0: description = "-description '%s'" % (description)
if authenticationAlias!=None and len(authenticationAlias.strip()) != 0: authenticationAlias = '-authDataAlias %s' % (authenticationAlias)
if xaRecoveryAuthAlias!=None and len(xaRecoveryAuthAlias.strip()) != 0: xaRecoveryAuthAlias = '-xaRecoveryAuthAlias %s' % (xaRecoveryAuthAlias)
if targetClient == 'JMS':
    print "JMS %s: Create %s in scope %s :" % (typeConnectionFactory,name,scopeName),
    try:
       AdminTask.createSIBJMSConnectionFactory(scopeid, ["-name %s -jndiName %s -busName %s %s %s %s %s" % (name,jndiName,JMSbusName,Type,description,authenticationAlias,xaRecoveryAuthAlias)]) 
       print "OK"
    except:
       print "KO"
       type, value, traceback = sys.exc_info()
       print "ERROR: %s (%s)" % (str(value), type)
       clearExit("Rollback and exit", -1)

elif targetClient == 'MQ':
    print "MQ %s: Create %s in scope %s :" % (typeConnectionFactory,name,scopeName),
    try:
       if MQqueueManager != None and len(MQqueueManager.strip()) != 0: MQqueueManager = '-qmgrName %s' % (MQqueueManager)
       if MQhostName != None and len(MQhostName.strip()) != 0: MQhostName = '-qmgrHostname %s' % (MQhostName)
       if MQtransportType != None and len(MQtransportType.strip()) != 0 : MQtransportType = '-wmqTransportType %s' % (MQtransportType)
       AdminTask.createWMQConnectionFactory(scopeid, ["-name %s -jndiName %s %s %s -qmgrPortNumber %s -qmgrSvrconnChannel %s %s %s %s %s %s" % (name,jndiName,MQqueueManager,MQhostName,MQport,MQchannel,Type,description,authenticationAlias,xaRecoveryAuthAlias,MQtransportType)]) 
       print "OK"
    except:
       print "KO"
       type, value, traceback = sys.exc_info()
       print "ERROR: %s (%s)" % (str(value), type)
       clearExit("Rollback and exit", -1)
else:
    print "TargetClient Not in Scope , No Action can Taken"
    
syncEnv(AdminConfig.hasChanges())
print "Create Connection Factory done"
# Done
print "%s V%s done" % (scriptName, version)
