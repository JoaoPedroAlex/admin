# Authors: Sergio Stinchi

# Version        Description
# 1.1.1          Removing mandatory for Queue Manager and changed check for resources
# 1.1.0          Correct Variable description
# 1.0.0          Starting version

# Import
import sys
import java
from string import replace

commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))

scopeName = ''               # mandatory [The name of the resource scope (i.e: Telematico, DogTelProNode01, ...)]
                             #            Warning: if the scope is a server and its name is not unique on the cell
                             #                     it must be used the form <Node>:<Server>
name = ''                    # mandatory [The name of the Activation Specification]     
jndiName = ''                # mandatory [The jndi of the Activation Specification]
destinationType = ''         # mandatory [Admitted values: javax.jms.Queue or javax.jms.Topic]
destinationJndiName = ''     # mandatory [The jndi of the Destination]
targetClient = ''            # mandatory [Admitted values: JMS or MQ]
authenticationAlias = ''     # optional
description = ''             # optional  [A description of the Activation Specification]
activationSpecClass = ''     # optional  [Read only]
deleteIfExist = 0            # 1 = delete the resource if exists

# JMS only
JMSbusName = ''              # mandatory [The bus of the Activation Specification]
JMSmaxBatchSize = ''         # optional
JMSmaxConcurrency = ''       # optional

# MQ only 
MQqueueManager =''           # optional  [The Queue Manager that hosts the Activation Specification] 
MQhostName =''               # optional  [hostname of the Queue Manager. If empty local host used]
MQport=''                    # optional  [port of the Queue Manager]
MQchannel=''                 # optional  [channel of the Queue Manager]
MQtransportType =''          # optional  [The way in which a connection is established to WebSphere MQ for this activation specification.
                             #            Admitted values: BINDINGS, BINDINGS_THEN_CLIENT or CLIENT. BINDINGS_THEN_CLIENT is the default value.]

was_stopEndpointIfDeliveryFails='true'
was_failureDeliveryCount='5'
# Variables
scriptName = "CreateActivationSpecs.py"
version = "1.1.1"

print "%s V%s" % (scriptName, version)


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

if (destinationType == None) or len(destinationType.strip()) == 0:
   print "ERROR: The variable destinationType is mandatory"
   print "%s done" % (scriptName)
   sys.exit(-1)
elif destinationType.strip() != 'javax.jms.Queue' and destinationType.strip() != 'javax.jms.Topic':
   print "ERROR: The variable destinationType has to be javax.jms.Queue or javax.jms.Topic"
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

if (destinationJndiName == None) or len(destinationJndiName.strip()) == 0:
   print "ERROR: The variable destinationJndiName is mandatory"
   print "%s done" % (scriptName)
   sys.exit(-1)

if targetClient == 'JMS':
   if (JMSbusName == None) or (len(JMSbusName.strip()) == 0):
      print "ERROR: The variable JMSbusName is mandatory"
      print "%s done" % (scriptName)
      sys.exit(-1)

   if (JMSmaxBatchSize == None) or len(JMSmaxBatchSize.strip()) != 0 :
      if JMSmaxBatchSize.strip().isdigit():
         if int(JMSmaxBatchSize) <=0:
            print "WARNING: The variable JMSmaxBatchSize has to be > 0. Using default 1"
            JMSmaxBatchSize = '1'
      else:
         print "WARNING: The variable JMSmaxBatchSize has to be numeric. Using default 1"
         JMSmaxBatchSize = '1'
          
   if (JMSmaxConcurrency != None) and len(JMSmaxConcurrency.strip()) != 0 :
      if JMSmaxConcurrency.strip().isdigit():
         if int(JMSmaxConcurrency) <=0:
            print "WARNING: The variable JMSmaxConcurrency has to be > 0. Using default 10"
            JMSmaxConcurrency = '10'
      else:
         print "WARNING: The variable JMSmaxConcurrency has to be numeric. Using default 10"
         JMSmaxConcurrency = '10'
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
   
   if (MQtransportType != None) and len(MQtransportType.strip()) != 0 :
      if MQtransportType.strip() not in ['BINDINGS', 'BINDINGS_THEN_CLIENT', 'CLIENT']:
         print "ERROR: The variable MQtransportType could be only ['BINDINGS', 'BINDINGS_THEN_CLIENT', 'CLIENT']"
         print "%s done" % (scriptName)
         sys.exit(-1)

   if was_stopEndpointIfDeliveryFails not in ['true','false']:
      print "ERROR: The variable was_stopEndpointIfDeliveryFails must be true or false"
      print "%s done" % (scriptName)
      sys.exit(-1)
   
   
   if not checkIsNumber(was_failureDeliveryCount):
      print "ERROR: The variable was_failureDeliveryCount must be a number"
      print "%s done" % (scriptName)
      sys.exit(-1)
else:
    clearExit("Type of activationSpec not Allowed",-1)
    
if deleteIfExist not in [0, 1]:
   print "ERROR: The variable deleteIfExist can be 0 or 1"
   print "%s done" % (scriptName)
   sys.exit(-1)
   
print "Check data read done"

# set default values
if name == None:
   name = 'AS' + name   
   print "Set default name = " + name

if jndiName == None:
   jndiName = 'jms/' + name   
   print "Set default jndiName = " + jndiName

# Check scopeName ...
print "Check scope %s ..." % (scopeName)
(scope, scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(scopeName)
# Create AS
print "Create AS ..."
#out = checkIfResourceExist(scopeid, name,'J2CActivationSpec')
#if out != None:
(resourceId , resourceName) = checkIfResourceExist(scopeid, name, "J2CActivationSpec")
if resourceId != None: 
   print "AS %s already exists" % name
   if deleteIfExist == 1:
      print "Delete existing AS:",
      try: 
#         AdminConfig.remove(out)
         AdminConfig.remove(resourceId)
         print "OK"
      except: clearExit("KO\nRollback and exit", -1)
   else: clearExit("", 0)   

print "Create %s:" % (name),
try:
   if description != None and len(description.strip()) != 0 : description = "-description '%s'" % (description)
   if authenticationAlias != None and len(authenticationAlias.strip()) != 0 : authenticationAlias = '-authenticationAlias %s' % (authenticationAlias)
   commonAttr = "-name '%s' -jndiName %s -destinationJndiName %s -destinationType %s %s %s" % (name, jndiName, destinationJndiName, destinationType, description, authenticationAlias)

   if targetClient == 'JMS':
      if JMSmaxBatchSize != None and len(JMSmaxBatchSize.strip()) != 0 : JMSmaxBatchSize = '-maxBatchSize %s' % (JMSmaxBatchSize)
      if JMSmaxConcurrency != None and  len(JMSmaxConcurrency.strip()) != 0 : JMSmaxConcurrency = '-maxConcurrency %s' % (JMSmaxConcurrency)
      otherAttr = "-busName '%s' %s %s" % (JMSbusName, JMSmaxBatchSize, JMSmaxConcurrency)
      AdminTask.createSIBJMSActivationSpec(scopeid, "[%s %s]" % (commonAttr, otherAttr)) 
   else:
      if MQqueueManager != None and len(MQqueueManager.strip()) != 0: MQqueueManager = '-qmgrName %s' % (MQqueueManager)
      if MQhostName != None and len(MQhostName.strip()) != 0: MQhostName = '-qmgrHostname %s' % (MQhostName)
      if MQport != None and len(MQport.strip()) != 0 : MQport = '-qmgrPortNumber %s' % (MQport)
      if MQchannel != None and len(MQchannel.strip()) != 0 : MQchannel = '-qmgrSvrconnChannel %s' % (MQchannel)
      if was_stopEndpointIfDeliveryFails != None and len(was_stopEndpointIfDeliveryFails.strip()) != 0 : was_stopEndpointIfDeliveryFails = '-stopEndpointIfDeliveryFails %s' %(was_stopEndpointIfDeliveryFails)
      if was_failureDeliveryCount != None and len(was_failureDeliveryCount.strip()) != 0 : was_failureDeliveryCount = '-failureDeliveryCount %s' %(was_failureDeliveryCount)
      if MQtransportType != None and len(MQtransportType.strip()) != 0 : MQtransportType = '-wmqTransportType %s' % (MQtransportType)
      otherAttr = "%s %s %s %s %s %s %s" % (MQqueueManager, MQhostName, MQport, MQchannel,was_stopEndpointIfDeliveryFails,was_failureDeliveryCount, MQtransportType)
      AdminTask.createWMQActivationSpec(scopeid, "[%s %s]" % (commonAttr, otherAttr)) 

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
