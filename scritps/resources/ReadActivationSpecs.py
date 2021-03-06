#! /usr/bin/python
# Authors: Sergio Stinchi

# Version        Description
# 1.4.0          Corrected error into main
# 1.3.0          Add Read Resources at cell Level
# 1.2.0          Add Outputh Path parameter
# 1.1.0          Modify input parameter
# 1.0.0          Starting version
from string import replace

commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))

global f, reportName

scriptName = "ReadActivationSpecs.py"
version = "1.4.0"

print "%s V%s" % (scriptName, version)

scopeName = ''              # mandatory, mandatory, the name of the scope resource (i.e: Telematico, DogTelProNode01, ...)
                            # Warning: if the scope is a server and its name is not unique on the cell
                            #          it must be used the form <Node>:<Server>
name = ''                   # mandatory
jndiName = ''               # mandatory
destinationJndiName = ''    # mandatory
authenticationAlias = ''    # optional
destinationJndiName = ''    # mandatory
description = ''            # optional
JMSmaxBatchSize = ''         
JMSmaxConcurrency = ''
busName = ''
parameters =''

deleteIfExist = 0           # 1 = delete the resource if exists

# Command Line
argc = len(sys.argv)
if argc != 2:
   print "Usage: %s <path output files> <scope> " % (scriptName)
   sys.exit(-1)

# Read target data file
print "Read target data file ..."
outputPath = sys.argv[0]
inputScopeName = sys.argv[1]

print "outputPath = %s" % (outputPath)
#print "inputScopeName = %s" % (inputScopeName)

#utility variable

# check parameter
print "Check Parameter .... "
if inputScopeName != 'ALL':
   (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(inputScopeName)

# Auxiliary functions
def clearExit(text, status):
   if len(text): print text
   AdminConfig.reset()
   print "%s done" % scriptName
   sys.exit(status)
   return

def listActivationSpec(ActivationSpecs_list, scopeId,scopeName,scopeType):
   for ActivationSpecs in ActivationSpecs_list.splitlines():
      if not isObjectInScope(ActivationSpecs,scopeName,scopeType):
         continue
      sc=getScopeResources(ActivationSpecs)
      JMSmaxBatchSize=''
      JMSmaxConcurrency=''
      JMSbusName=''
      MQchannel=''
      MQqueueManager=''
      MQhostName=''
      MQport=''
      destinationJndiName=''
      destinationType=''
      strProps=''
      arbitraryProperties=''
      was_stopEndpointIfDeliveryFails=''
      was_failureDeliveryCount=''
      MQtransportType=''
      print "     Found ActivationSpecs = %s " % (ActivationSpecs) 
      out = getScopeResources(ActivationSpecs)
      (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(out)
      partName = AdminConfig.showAttribute(ActivationSpecs, 'name')
      activationSpec = checkIfIsNone(AdminConfig.showAttribute(ActivationSpecs, 'activationSpec'))
      activationSpecClass = checkIfIsNone(AdminConfig.showAttribute(activationSpec, 'activationSpecClass'))
      if activationSpecClass =='com.ibm.ws.sib.api.jmsra.impl.JmsJcaActivationSpecImpl':
          activationSpecClass ='JMSActivationSpec'
          targetClient = 'JMS'
      elif activationSpecClass == 'com.ibm.mq.connector.inbound.ActivationSpecImpl':
          activationSpecClass ='MQActivationSpec'
          targetClient = 'MQ'
      else:
          print "ActivationSpec %s not managed " %(partName)
          continue
      fileName = "%s/%s.%s.%s.py" %(outputPath,replace(partName," ","_"),replace(sc,":","_"),activationSpecClass)
      fp = fileName
      displayList = []
      f = open(fileName, "w")
      # root properties
      name = checkIfIsNone(AdminConfig.showAttribute(ActivationSpecs, 'name'))
      jndiName = checkIfIsNone(AdminConfig.showAttribute(ActivationSpecs, 'jndiName'))
      authenticationAlias = checkIfIsNone(AdminConfig.showAttribute(ActivationSpecs, 'authenticationAlias'))
      if authenticationAlias==None: authenticationAlias=''
      destinationJndiName = checkIfIsNone(AdminConfig.showAttribute(ActivationSpecs, 'destinationJndiName'))
      description = checkIfIsNone(AdminConfig.showAttribute(ActivationSpecs, 'description'))
      propSet = wsadminToList(AdminConfig.showAttribute(ActivationSpecs, 'resourceProperties'))
      for prop in propSet:
         if AdminConfig.showAttribute(prop, 'name') == 'maxBatchSize':
            JMSmaxBatchSize =  AdminConfigShowAttribute(prop,'value')
         if AdminConfig.showAttribute(prop, 'name') == 'maxConcurrency':
            JMSmaxConcurrency  = AdminConfigShowAttribute(prop,'value')
         if AdminConfig.showAttribute(prop, 'name') == 'busName':
            JMSbusName = AdminConfigShowAttribute(prop,'value')    
         if AdminConfig.showAttribute(prop, 'name') == 'channel':
            MQchannel = AdminConfigShowAttribute(prop,'value')
         if AdminConfig.showAttribute(prop, 'name') == 'transportType':
            MQtransportType = AdminConfigShowAttribute(prop,'value')
         if AdminConfig.showAttribute(prop, 'name') == 'queueManager':
            MQqueueManager = AdminConfigShowAttribute(prop,'value')
            # Correzione per Bug WebSphere
            if MQqueueManager.find('-qmgrName') != -1:
               MQqueueManager =  MQqueueManager.split(" ")[1]
         if AdminConfig.showAttribute(prop, 'name') == 'hostName':
            MQhostName = AdminConfigShowAttribute(prop,'value')
         if AdminConfig.showAttribute(prop, 'name') == 'port':
            MQport = AdminConfigShowAttribute(prop,'value')
         if targetClient == 'MQ':
            if AdminConfig.showAttribute(prop, 'name') == 'destination':
               destinationJndiName = AdminConfigShowAttribute(prop,'value')
         if AdminConfig.showAttribute(prop, 'name') == 'destinationType':
            destinationType = AdminConfigShowAttribute(prop,'value')      
         #gestione number of fail
         if AdminConfigShowAttribute(prop, 'name') == 'arbitraryProperties':
            arbitraryProperties = AdminConfigShowAttribute(prop,'value')
            arbitraryPropertiesList = arbitraryProperties.split(",")
            was_stopEndpointIfDeliveryFails=str(arbitraryPropertiesList[0].split("=")[1])
            was_failureDeliveryCount=str(arbitraryPropertiesList[1].split("=")[1])
            #print "was_stopEndpointIfDeliveryFails= %s" %(was_stopEndpointIfDeliveryFails)
            #print "was_failureDeliveryCount= %s" %(was_failureDeliveryCount)
      displayList.append("scopeName='%s'" % (sc))
      displayList.append("name ='%s'" % (name))
      displayList.append("jndiName='" + jndiName + "'")
      displayList.append("authenticationAlias='%s'" % (authenticationAlias))
      displayList.append("destinationJndiName='%s'" % (destinationJndiName))
      displayList.append("description='" + str(description) + "'")
      displayList.append("JMSmaxBatchSize='%s'" %(JMSmaxBatchSize))
      displayList.append("JMSmaxConcurrency='%s'" %(JMSmaxConcurrency))
      displayList.append("JMSbusName='%s'" %(JMSbusName))
      displayList.append("MQchannel='%s'" %(MQchannel))
      displayList.append("MQqueueManager='%s'" %(MQqueueManager))
      displayList.append("MQhostName='%s'" %(MQhostName))
      displayList.append("MQport='%s'" %(MQport))
      displayList.append("MQtransportType='%s'" %(MQtransportType))
      displayList.append("destinationType='%s'" %(destinationType))
      displayList.append("targetClient='%s'" %(targetClient))
      if (was_stopEndpointIfDeliveryFails != None) and (len(was_stopEndpointIfDeliveryFails.strip()) != 0):
         displayList.append("was_stopEndpointIfDeliveryFails = %s"  %(was_stopEndpointIfDeliveryFails))
      if (was_failureDeliveryCount != None) and (len(was_failureDeliveryCount.strip()) != 0):
         displayList.append("was_failureDeliveryCount = %s"  %(was_failureDeliveryCount))
      displayList.append("deleteIfExist=1")
      #for prop in propSet:
      #   nm = AdminConfig.showAttribute(prop, 'name')
      #   vl = AdminConfigShowAttribute(prop,'value')
      #   strProps +=  " ['%s' ,'%s'], " %(nm,vl)
      #parameters = "parameters = [ %s ]" % (strProps)
      #displayList.append(parameters)
      void = display(displayList, f)
      f.close()
# end def


def launch(servers, nodes, clusters,cell):
   # List ActivationSpec  on CELL
   if len(cell) > 0:
        cellName = AdminConfig.showAttribute(cell[0], 'name')
        J2CActivationSpec_list = AdminConfig.list("J2CActivationSpec", cell[0])
        listActivationSpec(J2CActivationSpec_list,cell[0], cellName,"cells")
   
   # List ActivationSpec  on Server
   if len(servers) > 0:
      for server in servers:
         ServerName = getServerName(server)
         print "Retrieve Acivation Spec per server %s .. " % ServerName
         if checkIfIsServerTemplate(server) == False:
            NodeName = getNodeNameForServer(server)
            NodeServer = "%s:%s" % (NodeName, ServerName)
            (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(NodeServer) 
            if getServerType(nodeName,serverName) != 'NODE_AGENT' and getServerType(nodeName,serverName) != 'WEB_SERVER':
               J2CActivationSpec_list = AdminConfig.list('J2CActivationSpec', server)
               listActivationSpec(J2CActivationSpec_list,server, serverName,"servers")
   if len(nodes) > 0:
      for node in nodes:
         NodeName = AdminConfig.showAttribute(node, 'name')
         print "Retrieve J2CActivationSpec for server %s .. " % NodeName
         if not nodeIsDmgr(NodeName) and not nodeIsIHS(NodeName):
            J2CActivationSpec_list = AdminConfig.list('J2CActivationSpec',node)
            listActivationSpec(J2CActivationSpec_list, node, NodeName,"nodes")
   if len(clusters) > 0:
      for cluster in clusters:
         ClusterName = AdminConfig.showAttribute(cluster, 'name')
         print "Retrieve J2CActivationSpec for Cluster %s .. " % ClusterName
         J2CActivationSpec_list = AdminConfig.list('J2CActivationSpec', cluster)
         listActivationSpec(J2CActivationSpec_list, cluster,ClusterName,"clusters")
# End Def
    

if inputScopeName == 'ALL':
   cell=AdminConfig.list("Cell").splitlines()
   servers = AdminConfig.list('Server').splitlines()
   nodes = AdminConfig.list('Node').splitlines()
   clusters = AdminConfig.list('ServerCluster').splitlines()
   launch(servers, nodes, clusters,cell)
elif scope == 'Cell': 
    cell=[scopeid]
    servers = []
    nodes = []
    clusters = []
    launch(servers, nodes, clusters,cell)
elif scope == 'Server':
    cell=[]
    servers = [scopeid]
    nodes = []
    clusters = []
    launch(servers, nodes, clusters,cell)
elif scope == 'Node':
    cell=[]
    servers = []
    nodes = [scopeid]
    clusters = []
    launch(servers, nodes, clusters,cell)
elif scope == 'ServerCluster':
    cell=[]
    servers = []
    nodes = []
    clusters = [scopeid]
    launch(servers, nodes, clusters,cell)


print "%s V%s done" % (scriptName, version)



