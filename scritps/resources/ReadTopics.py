# Authors: Sergio Stinchi

# Version        Description
# 1.0.0          Starting version



from string import replace

commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))

global f, reportName


scriptName = "ReadTopics.py"
version = "1.0.0"

def getJ2CAdminObjectType(obj):
   try:
      adminObject=AdminConfig.showAttribute((obj),'adminObject') 
      J2CAdminObjectType=AdminConfig.showAttribute(adminObject,'adminObjectInterface')
      print "J2CAdminObjectType: %s " % (J2CAdminObjectType)
   except:        
      J2CAdminObjectType = ''  
   return J2CAdminObjectType


print "%s V%s" % (scriptName, version)

# Command Line
argc = len(sys.argv)
if argc != 2:
   print "Usage: %s <path output files> <scope> " % (scriptName)
   sys.exit(-1)

# Read target data file
print "Read target data file ..."
outputPath = sys.argv[0]
inputScopeName = sys.argv[1]

# print "outputPath = %s" % (outputPath)
# print "inputScopeName = %s" % (inputScopeName)

# check parameter
print "Check Parameter .... "
if inputScopeName != 'ALL':
   (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(inputScopeName)


def listSIBJMSTopic(JMSTopic_list, scopeId,scopeName,scopeType):  
   BusName = ""
   TopicName = ""
   for JMSTopic in JMSTopic_list.splitlines():
      if not isObjectInScope(JMSTopic,scopeName,scopeType):
         continue
      sc = getScopeResources(JMSTopic)
      BusName = ''
      partName = AdminConfigShowAttribute(JMSTopic, 'name')
      if getJ2CAdminObjectType(JMSTopic) == 'javax.jms.Topic':
         print "     found JMSTopic = %s " % (partName)
      else:
         print "     The object found = %s it is not a JMSTopic, SKIPPING" % (partName)
         continue
      out = getScopeResources(JMSTopic)
      # print "out = %s" %(out)
      (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(out)
      if not os.path.exists(outputPath): clearExit("Output Path Not Found - Rollback and exit", -1)
      fileName = "%s/%s.%s.%s.py" % (outputPath, replace(partName, " ", "_"), replace(sc, ":", "_"), getTypeName(JMSTopic))
      fp = fileName
      displayList = []
      f = open(fileName, "w")
      name = AdminConfigShowAttribute(JMSTopic, 'name')
      jndiName = AdminConfigShowAttribute(JMSTopic, 'jndiName')
      description = AdminConfigShowAttribute(JMSTopic, 'description')
      propSet = wsadminToList(AdminConfigShowAttribute(JMSTopic, 'properties'))
      for prop in propSet:
         if AdminConfigShowAttribute(prop, 'name') == 'TopicName':
            TopicName = AdminConfigShowAttribute(prop, 'value')
         if AdminConfigShowAttribute(prop, 'name') == 'BusName':
            BusName = AdminConfigShowAttribute(prop, 'value')  
         if AdminConfigShowAttribute(prop, 'name') == 'TopicSpace':
            TopicSpace = AdminConfigShowAttribute(prop, 'value')  
         if AdminConfigShowAttribute(prop, 'name') == 'DeliveryMode':
            DeliveryMode = AdminConfigShowAttribute(prop, 'value')  
      # Common value for JMS and MQ
      displayList.append("scopeName='%s'" % (sc))
      displayList.append("name='%s'" % (name))
      displayList.append("jndiName='%s'" % (str(jndiName)))
      displayList.append("TopicName='%s'" % (TopicName))
      displayList.append("description='%s'" % (str(description)))
      displayList.append("targetClient='%s'" % ('JMS'))
      displayList.append("TopicSpace='%s'" % (TopicSpace))
      displayList.append("DeliveryMode='%s'" % (DeliveryMode))
      # Specific For JMS
      displayList.append("busName='%s'" % (BusName))
      displayList.append("deleteIfExist=1")
      void = display(displayList, f)
      f.close()
# end def

def listMQTopic(MQTopic_list, scopeId,scopeName,scopeType):
   for MQTopic in MQTopic_list.splitlines():
      if not isObjectInScope(MQTopic,scopeName,scopeType):
         continue
      sc = getScopeResources(MQTopic)
      partName = AdminConfigShowAttribute(MQTopic, 'name')
      print "     found MQTopic = %s " % (partName)
      out = getScopeResources(MQTopic)
      (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(out)
      fileName = "%s/%s.%s.%s.py" % (outputPath, replace(partName, " ", "_"), replace(sc, ":", "_"), getTypeName(MQTopic))
      displayList = []
      f = open(fileName, "w")
      queueName = AdminConfigShowAttribute(MQTopic, 'baseQueueName')
      jndiName = AdminConfigShowAttribute(MQTopic, 'jndiName')
      description = AdminConfigShowAttribute(MQTopic, 'description')
      persistence = AdminConfigShowAttribute(MQTopic, 'persistence')
      providerID = AdminConfigShowAttribute(MQTopic, 'provider')
      baseQueueManagerName = AdminConfigShowAttribute(MQTopic, 'baseQueueManagerName')
      queueManagerPort = AdminConfigShowAttribute(MQTopic, 'queueManagerPort')
      queueManagerHost = AdminConfigShowAttribute(MQTopic, 'queueManagerHost')
      serverConnectionChannelName = AdminConfigShowAttribute(MQTopic, 'serverConnectionChannelName')
      userName = AdminConfigShowAttribute(MQTopic, 'userName')
      password = AdminConfigShowAttribute(MQTopic, 'password')
      targetClient = AdminConfigShowAttribute(MQTopic, 'targetClient')
      # Common value for JMS and MQ
      displayList.append("scopeName='%s'" % (sc))
      displayList.append("name='%s'" % (partName))
      displayList.append("jndiName='%s'" % (jndiName))
      displayList.append("queueDestName='%s'" % (queueName))
      displayList.append("description='%s'" % (description))
      displayList.append("targetClient='%s'" % ('MQ'))
      # Specific for MQ Topic
      displayList.append("baseQueueManagerName='%s'" % (baseQueueManagerName))
      displayList.append("persistence='%s'" % (persistence))
      displayList.append("providerID=%s" % (providerID))
      displayList.append("queueManagerHost ='%s'" % (queueManagerHost))
      displayList.append("queueManagerPort='%s'" % (queueManagerPort))
      displayList.append("serverConnectionChannelName='%s'" % (serverConnectionChannelName))
      displayList.append("userName='%s'" % (userName))
      displayList.append("deleteIfExist=1")
      void = display(displayList, f)
      f.close()


# il nome del server quando è uguale al nome del cluster è di tipo serverTemplate
def launch(servers, nodes, clusters, cell):
   if len(cell) > 0:
        cellName = AdminConfig.showAttribute(cell[0], 'name')
        JMSTopic_list = AdminConfig.list('J2CAdminObject', cell[0])
        listSIBJMSTopic(JMSTopic_list, cell[0], cellName, "cells")
        MQTopic_list = AdminConfig.list('MQTopic', cell[0])
        listMQTopic(MQTopic_list, cell[0], cellName, "cells")
   
   if len(servers) > 0:
      for server in servers:
         ServerName = getServerName(server)
         print "Retrieve Topic for server %s .. " % (ServerName)
         if checkIfIsServerTemplate(server) == False:
            nodeName = getNodeNameForServer(server)
            NodeServer = "%s:%s" % (nodeName, ServerName)
            (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(NodeServer)
            if getServerType(nodeName, serverName) != 'NODE_AGENT' and getServerType(nodeName, serverName) != 'WEB_SERVER':
               JMSTopic_list = AdminConfig.list('J2CAdminObject', server)
               listSIBJMSTopic(JMSTopic_list, server, serverName, 'servers')
               MQTopic_list = AdminConfig.list('MQTopic', server)
               listMQTopic(MQTopic_list, server, serverName, 'servers')
         else:
             print " %s is a Dynamic Cluster Server Template " % (server)
   if len(nodes) > 0:
      for node in nodes:
         nodeName = AdminConfigShowAttribute(node, 'name')
         print "Retrieve Topic for Node %s .. " % nodeName
         if not nodeIsDmgr(nodeName) and not nodeIsIHS(nodeName):
            JMSTopic_list = AdminConfig.list('J2CAdminObject', node)
            listSIBJMSTopic(JMSTopic_list, node, nodeName, 'nodes')
            MQTopic_list = AdminConfig.list('MQTopic', node)
            listMQTopic(MQTopic_list, node, nodeName, 'nodes')
   if len(clusters) > 0:
      for cluster in clusters:
         ClusterName = AdminConfigShowAttribute(cluster, 'name')
         print "Retrieve Topic for Cluster %s .. " % ClusterName
         JMSTopic_list = AdminConfig.list('J2CAdminObject', cluster)
         listSIBJMSTopic(JMSTopic_list,cluster,ClusterName,'clusters')
         MQTopic_list = AdminConfig.list('MQTopic', cluster)
         listMQTopic(MQTopic_list,cluster,ClusterName,'clusters')

# End Def
# inizialize parameter    
cell = []
servers = []
nodes = []
clusters = []
if inputScopeName == 'ALL':
   cell=AdminConfig.list("Cell").splitlines()
   servers = AdminConfig.list('Server').splitlines()
   nodes = AdminConfig.list('Node').splitlines()
   clusters = AdminConfig.list('ServerCluster').splitlines()
   launch(servers, nodes, clusters, cell)   
   
elif scope == 'Cell':
   cell = [scopeid]
   launch(servers, nodes, clusters, cell)
elif scope == 'Server':
    servers = [scopeid]
    launch(servers, nodes, clusters, cell)
elif scope == 'Node':
    nodes = [scopeid]
    launch(servers, nodes, clusters, cell)
elif scope == 'ServerCluster':
    clusters = [scopeid]
    launch(servers, nodes, clusters, cell)



print "%s V%s done" % (scriptName, version)
