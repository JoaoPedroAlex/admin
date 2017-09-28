#! /usr/bin/python
# Authors: Sergio Stinchi

# Version        Description
# 1.3.0          Managed provider type when it finishes with " XA)" in addition to " (XA)"
# 1.2.0          Add Read Resources at cell Level
# 1.1.0          Modify print function
# 1.0.0          Starting version


# Import

import java
from string import replace

global f, reportName


commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))

# Variables
scriptName = "ReadJDBCProvider.py"
version = "1.3.0"



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

#print "outputPath = %s" %(outputPath)
#print "inputScopeName = %s" %(inputScopeName)


#check parameter
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

def listJDBCProvider(JDBCProv_list, scopeId,scopeName,scopeType):
   configurationParameters = ""
   for JDBCProv in JDBCProv_list.splitlines():
      if not isObjectInScope(JDBCProv,scopeName,scopeType):
         continue
      sc=getScopeResources(JDBCProv)
      print "     found JDBCProvider = %s " % (JDBCProv)
      partName = AdminConfigShowAttribute(JDBCProv, 'name')
      scopeName = AdminConfigShowAttribute(scopeId, 'name')    
      # print "scopeName = %s " %(scopeName) 
      if not os.path.exists(outputPath): clearExit("Output Path Not Found - Rollback and exit",-1)
      pName = replace(partName, " ", "_")
      pName = replace(pName, "(", "")
      pName = replace(pName, ")", "")
      pScopeName =replace(sc, ":", "_")
      fileName = "%s.%s.JDBCProvider.py" % (pName, pScopeName)
      #print "Create File %s for JDBCProv %s " % (fileName, partName)
      fp = fileName
      displayList = []
      f = open(str(outputPath) + "/"+ str(fileName), "w")
      classpath=AdminConfigShowAttribute(JDBCProv,'classpath')
      description=AdminConfigShowAttribute(JDBCProv,'description')
      implementationClassName=AdminConfigShowAttribute(JDBCProv,'implementationClassName')
      isolated=AdminConfigShowAttribute(JDBCProv,'isolatedClassLoader')
      name=AdminConfigShowAttribute(JDBCProv,'name')
      nativepath=AdminConfigShowAttribute(JDBCProv,'nativepath')
      providerType=AdminConfigShowAttribute(JDBCProv,'providerType')
      if providerType.find(" (XA)") !=-1: 
         providerType = providerType.split(" (XA)")[0]
      elif providerType.find(" XA)") !=-1: 
         providerType = providerType.split(" XA)")[0] + ")"
      xa=AdminConfigShowAttribute(JDBCProv,'xa')
      webSphereVars=[]
      databaseType = getProviderType(JDBCProv)     
      displayList.append("scopeName='%s'" % (sc))
      displayList.append("classpath='%s'" % (classpath))
      displayList.append("description='%s'" % (description))
      displayList.append("implementationClassName='%s'" % (implementationClassName))
      displayList.append("isolated='%s'" % (isolated))
      displayList.append("name='%s'" % (name))
      displayList.append("nativePath='%s'" % (nativepath))
      displayList.append("providerType='%s'" % (providerType))
      displayList.append("databaseType='%s'" % (databaseType))
      displayList.append("xa='%s'" % (xa))
      displayList.append("webSphereVars=%s" % (webSphereVars))
      displayList.append("deleteIfExist=1")
      void = display(displayList, f)
      f.close()
# end def

def launch(servers,nodes,clusters,cell):
   if len(cell) > 0:
        cellName = AdminConfig.showAttribute(cell[0], 'name')
        JDBCProvs_list = AdminConfig.list("JDBCProvider", cell[0])
        listJDBCProvider(JDBCProvs_list,cell[0], cellName,"cells")
   # List JDBCProvider on Servers
   if len(servers) > 0:
      for server in servers:
        ServerName = getServerName(server)
        print "Retrieve JDBC Provider per server %s .. " % ServerName
        if checkIfIsServerTemplate(server) == False:
           NodeName = getNodeNameForServer(server)
           NodeServer = "%s:%s" % (NodeName, ServerName)
           (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(NodeServer) 
           if getServerType(nodeName,serverName) != 'NODE_AGENT' and getServerType(nodeName,serverName) != 'WEB_SERVER':
              JDBCProvs_list = AdminConfig.list("JDBCProvider", server)
              listJDBCProvider(JDBCProvs_list, server, ServerName,"servers")
   # List JDBCProvider on Nodes
   if len(nodes) > 0:
      for node in nodes:
         NodeName = AdminConfigShowAttribute(node, 'name')
         print "Retrieve JDBCProvider for node %s .. " % NodeName
         if not nodeIsDmgr(NodeName) and not nodeIsIHS(NodeName):
            JDBCProvs_list = AdminConfig.list("JDBCProvider", node)
            listJDBCProvider(JDBCProvs_list, node,NodeName,'nodes')
   # List JDBCProvider on Cluster
   if len(clusters) > 0:
      for cluster in clusters:
         ClusterName = AdminConfigShowAttribute(cluster, 'name')
         print "Retrieve JDBCProvider for cluster %s .. " % ClusterName 
         JDBCProvs_list = AdminConfig.list("JDBCProvider", cluster)
         listJDBCProvider(JDBCProvs_list, cluster,ClusterName,'clusters')
#End Def
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
   launch(servers,nodes,clusters,cell)
elif scope == 'Cell':
    cell=[scopeid]
    launch(servers, nodes, clusters,cell)
elif scope =='Server':
    servers = [scopeid]
    launch(servers, nodes, clusters,cell)
elif scope =='Node':
    nodes = [scopeid]
    launch(servers, nodes, clusters,cell)
elif scope == 'ServerCluster':
    clusters = [scopeid]
    launch(servers, nodes, clusters,cell)
      
print "%s V%s done" % (scriptName, version)
