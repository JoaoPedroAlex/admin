#!/usr/bin/python
# Authors: Sergio Stinchi

# Version   Changed by     			Description
# 1.4.0		Joao Pedro Alexandre	Add code to be able to run in unmanaged node, I have to replace the function getDmgrNodeName by another to get the node name 
#									in an unmanaged node
#									Add code to list also Microsoft datasources
# 1.3.0          					Add Read Resources at cell Level
# 1.2.0          					Modify Properties name File
# 1.1.0          					Add CheckDataSOurces for Server
# 1.0.0          					Starting version

# Import
import sys
import java
from string import replace
global f, reportName

commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))

# Variables
scriptName = "ReadDataSources.py"
version = "1.4.0"

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

print "outputPath = %s" % (outputPath)
print "inputScopeName = %s" % (inputScopeName)

# check parameter
print "Check Parameter .... "
if inputScopeName != 'ALL':
   (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(inputScopeName)

   
def listDataSources(DS_list, scopeId,scopeName,scopeType):
   configurationParameters = ""
   for DS in DS_list.splitlines():
      if not isObjectInScope(DS,scopeName,scopeType):
          continue
      sc=getScopeResources(DS)
      partName = AdminConfig.showAttribute(DS, 'name')
      print "sc= %s " %(sc)
      print "partName= %s " %(partName)
      fileName = "%s/%s.%s.DS.py" % (outputPath, replace(partName, " ", "_"), replace(sc, ":", "_"))
      # print "Create File %s for Datasource %s " % (fileName,partName)
      fp = fileName
      displayList = []
      name = AdminConfig.showAttribute(DS, 'name')
      authDataAlias = AdminConfig.showAttribute(DS, 'authDataAlias')
      xaRecoveryAuthAlias = AdminConfig.showAttribute(DS, 'xaRecoveryAuthAlias')
      if authDataAlias == None:authDataAlias = ''
      if xaRecoveryAuthAlias == None:xaRecoveryAuthAlias = ''
      authMechanismPreference = AdminConfig.showAttribute(DS, 'authMechanismPreference')
      category = AdminConfig.showAttribute(DS, 'category')
      print "Category == %s " %(category)
      if category == 'default':
          print "    Default DataSource %s not included" % (name)
      else:
          print "     found DataSource = %s " % (DS) 
          f = open(fileName, "w")
          datasourceHelperClassname = AdminConfig.showAttribute(DS, 'datasourceHelperClassname')
          print "  datasourceHelperClassname = %s " % (datasourceHelperClassname)
          provider = AdminConfig.showAttribute(DS, 'provider')
          print "  provider = %s " % (provider)
          providerName = AdminConfig.showAttribute(provider, 'name')
          print "  providerName = %s " % (providerName)
          description = AdminConfig.showAttribute(DS, 'description')
          print "  description = %s " % (description)
          jndiName = AdminConfig.showAttribute(DS, 'jndiName')
          print "  jndiName = %s " % (jndiName)
          statementCacheSize = AdminConfig.showAttribute(DS, 'statementCacheSize')
          print "  statementCacheSize = %s " % (statementCacheSize)
          authenticationUsername = "USER_TO_CHANGE"
          authenticationPassword = "PASSWORD_TO_CHANGEE"
          authenticationDescription = "Description Authentication to change"
          displayList.append("scopeName='%s'" %(sc))
          displayList.append("name='%s'" % (name))
          displayList.append("jndiName='%s'" % (jndiName))
          displayList.append("dataStoreHelperClassName='%s'" % (datasourceHelperClassname))
#Comment next line to be able to run in unmanaged node, I have to replace the function getDmgrNodeName by another to get the node name in an unmanaged node
#         authDataAlias = replace(authDataAlias, getDmgrNodeName() + '/', '')
# added these lines From here
#          dmgrNode = getDmgrNodeName()
#          if dmgrNode is None:
#             NodeName = getNodeNameForServer(scopeName)
#          else:
#             NodeName = dmgrNode
# the previous code have some problems, error message:
# WASX7444E: Invalid parameter value "null" for parameter "config id" on command "showAttribute"
# replaced by next line: 
          NodeName = getNodeNameForServer(scopeName)
          authDataAlias = replace(authDataAlias, NodeName + '/', '')
# added these lines to here
          displayList.append("authenticationAlias='%s'" % (authDataAlias))
          displayList.append("authMechanismPreference='%s'" % (authMechanismPreference))
          displayList.append("providerName='%s'" % (providerName))
          displayList.append("authenticationUsername='%s'" % (authenticationUsername))
          displayList.append("authenticationPassword='%s'" % (authenticationPassword))
          displayList.append("authenticationDescription='%s'" % (authenticationDescription))
          if category != None:displayList.append("category='%s'" % (category))
#changed next line to be able to run in unmanaged node
#         xaRecoveryAuthAlias = replace(xaRecoveryAuthAlias, getDmgrNodeName() + '/', '')
          print " xaRecoveryAuthAlias before replace: %s " % xaRecoveryAuthAlias
          xaRecoveryAuthAlias = replace(xaRecoveryAuthAlias, NodeName + '/', '')
          print " xaRecoveryAuthAlias after replace: %s " % xaRecoveryAuthAlias
          displayList.append("xaRecoveryAuthAlias='%s'" % (xaRecoveryAuthAlias))
          displayList.append("containerManagedPersistence='%s'" % ('false'))
          if description != None:displayList.append("description='%s'" % (description))
          displayList.append("statementCacheSize='%s'" % (statementCacheSize))
          print "Provider: %s .. " % provider
          providerType = getProviderType(provider)
          propertySet = AdminConfig.showAttribute(DS, 'propertySet')
          resourceProperties = AdminConfig.showAttribute(propertySet, 'resourceProperties')[1:-1].split()
          propSetMap = convertListToHashMap(resourceProperties)
          print "ProviderType: %s .. " % providerType
          if (providerType == 'DB2'):
             driverType = propSetMap.get('driverType') 
             databaseName = propSetMap.get('databaseName') 
             serverName = propSetMap.get('serverName') 
             portNumber = propSetMap.get('portNumber')
             configurationParameters = " [ "
             configurationParameters += " ['%s','%s','%s']  " % ("databaseName", "java.lang.String", databaseName) 
             configurationParameters += ", ['%s','%s','%s']  " % ("serverName", "java.lang.String", serverName)
             configurationParameters += ", ['%s','%s','%s']  " % ("portNumber", "java.lang.Integer", portNumber) 
             configurationParameters += ", ['%s','%s','%s']  " % ("driverType", "java.lang.Integer", driverType)
             configurationParameters += " ] " 
             displayList.append("configurationParameters=%s" % (configurationParameters)) 
             # displayList.append("DB2.driverType='%s'" % (driverType))
             # displayList.append("DB2.databaseName='%s'" % (databaseName))
             # displayList.append("DB2.serverName='%s'" % (serverName))
             # displayList.append("DB2.portNumber='%s'" % (portNumber))
          elif (providerType == 'SQL Server'):
             driverType = propSetMap.get('driverType') 
             databaseName = propSetMap.get('databaseName') 
             serverName = propSetMap.get('serverName') 
             portNumber = propSetMap.get('portNumber')
             configurationParameters = " [ "
             configurationParameters += " ['%s','%s','%s']  " % ("databaseName", "java.lang.String", databaseName) 
             configurationParameters += ", ['%s','%s','%s']  " % ("serverName", "java.lang.String", serverName)
             configurationParameters += ", ['%s','%s','%s']  " % ("portNumber", "java.lang.Integer", portNumber)
             configurationParameters += " ] " 
             displayList.append("configurationParameters=%s" % (configurationParameters)) 
          elif (providerType == 'Oracle'):
             URL = propSetMap.get('URL')
             configurationParameters = "[ ['%s','%s','%s'] ] " % ("URL", "java.lang.String", URL) 
             displayList.append("configurationParameters=%s" % (configurationParameters)) 
          elif (providerType == 'Derby'):
             databaseName = propSetMap.get('databaseName') 
             configurationParameters = "[ ['%s','%s','%s'] ] " % ("databaseName", "java.lang.String", databaseName) 
             displayList.append("configurationParameters=%s" % (configurationParameters)) 
          optConfigurationParameters = []
          displayList.append("optConfigurationParameters=%s" % (optConfigurationParameters))
          connectionPool = AdminConfig.showAttribute(DS, 'connectionPool')
          agedTimeout = AdminConfig.showAttribute(connectionPool, 'agedTimeout')
          connectionTimeout = AdminConfig.showAttribute(connectionPool, 'connectionTimeout')
          maxConnections = AdminConfig.showAttribute(connectionPool, 'maxConnections')
          minConnections = AdminConfig.showAttribute(connectionPool, 'minConnections')
          purgePolicy = AdminConfig.showAttribute(connectionPool, 'purgePolicy')
          reapTime = AdminConfig.showAttribute(connectionPool, 'reapTime')
          unusedTimeout = AdminConfig.showAttribute(connectionPool, 'unusedTimeout')
          displayList.append("agedTimeout='%s'" % (agedTimeout))
          displayList.append("connectionTimeout='%s'" % (connectionTimeout))
          displayList.append("maxConnections='%s'" % (maxConnections))
          displayList.append("minConnections='%s'" % (minConnections))
          displayList.append("purgePolicy='%s'" % (purgePolicy))
          displayList.append("reapTime='%s'" % (reapTime))
          displayList.append("unusedTimeout='%s'" % (unusedTimeout))
          displayList.append("deleteIfExist=1")
          void = display(displayList, f)
          f.close()
# end def



def launch(servers, nodes, clusters,cell):
    # List DataSource on CELL
    if len(cell) > 0:
        cellName = AdminConfig.showAttribute(cell[0], 'name')
        DS_list = AdminConfig.list("DataSource", cell[0])
        listDataSources(DS_list, cell[0], cellName,"cells")

    # List DataSource on Servers
    if len(servers) > 0:
       for server in servers:
          serverName = getServerName(server)
          print "Retrieve DataSources per server %s .. " % serverName
          if checkIfIsServerTemplate(server) == False:
             NodeName = getNodeNameForServer(server)
             NodeServer = "%s:%s" % (NodeName, serverName)
             (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(NodeServer) 
             if getServerType(nodeName,serverName) != 'NODE_AGENT' and getServerType(nodeName,serverName) != 'WEB_SERVER':
                DS_list = AdminConfig.list("DataSource", server)
                listDataSources(DS_list, server, serverName,"servers")
    
    # List DataSource on Nodes
    if len(nodes) > 0:
       for node in nodes:
          NodeName = AdminConfig.showAttribute(node, 'name')
          print "Retrieve DataSource for node %s .. " % NodeName
          if not nodeIsDmgr(NodeName) and not nodeIsIHS(NodeName):
             DS_list = AdminConfig.list("DataSource", node)
             listDataSources(DS_list, node, NodeName,"nodes")
    
    
    # List DataSource on Cluster
    if len(clusters) > 0:
       for cluster in clusters:
          ClusterName = AdminConfig.showAttribute(cluster, 'name')
          print "Retrieve DataSource for cluster %s .. " % ClusterName 
          DS_list = AdminConfig.list("DataSource", cluster)
          listDataSources(DS_list, cluster,ClusterName,"clusters")
# End Def
#inizialize parameter 
cell=[]
servers = []
nodes = []
clusters = []
if inputScopeName == 'ALL':
   cell=AdminConfig.list("Cell").splitlines()
   servers = AdminConfig.list('Server').splitlines()
   nodes = AdminConfig.list('Node').splitlines()
   clusters = AdminConfig.list('ServerCluster').splitlines()
   launch(servers, nodes, clusters,cell)
elif scope == 'Cell':
    cell=[scopeid]
    launch(servers, nodes, clusters,cell)
elif scope == 'Server':
    servers = [scopeid]
    launch(servers, nodes, clusters,cell)
elif scope == 'Node':
    nodes = [scopeid]
    launch(servers, nodes, clusters,cell)
elif scope == 'ServerCluster':
    clusters = [scopeid]
    launch(servers, nodes, clusters,cell)



      
print "%s V%s done" % (scriptName, version)
