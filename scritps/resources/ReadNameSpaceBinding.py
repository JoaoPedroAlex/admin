#!/usr/bin/python
# Version        Description
# 1.4.0          Add Read Resources at cell Level
# 1.2.0          Add Read Properties fro NameSpaceBinding for server
# 1.1.0          Add StringNameSpaceBinding check
# 1.0.0          Starting version

import sys
import java
from string import replace

commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))

# Variables
scriptName = "ReadNameSpaceBinding.py"
version = "1.4.0"

print "%s V%s" % (scriptName, version)

global f, reportName

# Command Line
argc = len(sys.argv)
if argc != 2:
   print "Usage: %s <path output files> <scope> " % (scriptName)
   sys.exit(-1)

# Read target data file
print "Read target data file ..."
outputPath = sys.argv[0]
inputScopeName = sys.argv[1]

print "outputPath = %s" %(outputPath)
print "inputScopeName = %s" %(inputScopeName)

#check parameter
print "Check Parameter .... "
if inputScopeName != 'ALL':
   (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(inputScopeName)

def getNameSpaceBingingType(nmsp_id):
    beg = nmsp_id.find('#') + 1
    end = nmsp_id.find(')', beg)
    out = nmsp_id[beg:end]    
    return out.split('_')[0]


   
   
def listNameSpaceBinding(NameSpaceBinding_list, scopeId,scopeName,scopeType):
   configurationParameters = ""
   for NameSpaceBinding in NameSpaceBinding_list.splitlines():
      if not isObjectInScope(NameSpaceBinding,scopeName,scopeType):
         continue 
      partName = AdminConfig.showAttribute(NameSpaceBinding, 'name')
      print "   Found NameSpaceBinding << %s >> " %(partName)
      typeNameSpaceBinding = getNameSpaceBingingType(NameSpaceBinding)
      sc = getScopeResources(NameSpaceBinding)
      fileName = "%s/%s.%s.NSB.py" %(outputPath,replace(partName," ","_"),replace(sc,":","_"))
      #print "Create File %s for NameSpaceBinding %s " % (fileName, partName)
      fp = fileName
      displayList = []
      f = open(fileName, "w")
      displayList.append("scopeName='%s'" % (sc))
      displayList.append("typeNameSpaceBinding='%s'" % (typeNameSpaceBinding))
      #print "typeNameSpaceBinding = %s " %(typeNameSpaceBinding)
      if typeNameSpaceBinding == "StringNameSpaceBinding":
         name = AdminConfig.showAttribute(NameSpaceBinding, 'name')
         nameInNameSpace = AdminConfig.showAttribute(NameSpaceBinding, 'nameInNameSpace')
         stringToBind = AdminConfig.showAttribute(NameSpaceBinding, 'stringToBind')
         displayList.append("name='%s'" % (name))
         displayList.append("nameInNameSpace='%s'" % (nameInNameSpace))
         displayList.append("stringToBind='%s'" % (stringToBind))
      elif typeNameSpaceBinding == "EjbNameSpaceBinding":
          applicationNodeName = AdminConfig.showAttribute(NameSpaceBinding, 'applicationNodeName')
          applicationServerName = AdminConfig.showAttribute(NameSpaceBinding, 'applicationServerName')
          bindingLocation = AdminConfig.showAttribute(NameSpaceBinding, 'bindingLocation')
          ejbJndiName = AdminConfig.showAttribute(NameSpaceBinding, 'ejbJndiName')
          name = AdminConfig.showAttribute(NameSpaceBinding, 'name')
          nameInNameSpace = AdminConfig.showAttribute(NameSpaceBinding, 'nameInNameSpace')
          if applicationNodeName != None:displayList.append("applicationNodeName='%s'" % (applicationNodeName))
          displayList.append("applicationServerName='%s'" % (applicationServerName))
          displayList.append("bindingLocation='%s'" % (bindingLocation))
          displayList.append("ejbJndiName='%s'" % (ejbJndiName))
          displayList.append("name='%s'" % (name))
          displayList.append("nameInNameSpace='%s'" % (nameInNameSpace))         
      elif typeNameSpaceBinding == "IndirectLookupNameSpaceBinding":
         print "IndirectLookupNameSpaceBinding %s " % (NameSpaceBinding)
      elif typeNameSpaceBinding == "CORBAObjectNameSpaceBinding":
         print "CORBAObjectNameSpaceBinding %s " % (CORBAObjectNameSpaceBinding)
      else:
          print "ERROR: No Type Binding Found"
      displayList.append("deleteIfExist=1")
      void = display(displayList, f)
      f.close()
# end def


def launch(servers,nodes,clusters,cell):


    if len(cell) > 0:
        cellName = AdminConfig.showAttribute(cell[0], 'name')
        NameSpaceBinding_list = AdminConfig.list("NameSpaceBinding", cell[0])
        listNameSpaceBinding(NameSpaceBinding_list,cell[0], cellName,"cells")

# List NamespaceBinding on Servers
    if len(servers) > 0:
       for server in servers:
         ServerName = getServerName(server)
         print "Retrieve Queue for server %s .. " % (ServerName)
         if checkIfIsServerTemplate(server) == False:
            NodeName = getNodeNameForServer(server)
            NodeServer = "%s:%s" % (NodeName, ServerName)
            (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(NodeServer)
            if getServerType(nodeName,serverName) != 'NODE_AGENT' and getServerType(nodeName,serverName) != 'WEB_SERVER':
                NameSpaceBinding_list = AdminConfig.list("NameSpaceBinding", server)
                listNameSpaceBinding(NameSpaceBinding_list, server, ServerName,"servers")
    
    # List NamespaceBinding on Nodes
    if len(nodes) > 0:
       for node in nodes:
          NodeName = AdminConfig.showAttribute(node, 'name')
          print "Retrieve NameSpaceBinding per node %s .. " % NodeName
          if not nodeIsDmgr(NodeName) and not nodeIsIHS(NodeName):
             NameSpaceBinding_list = AdminConfig.list("NameSpaceBinding", node)
             listNameSpaceBinding(NameSpaceBinding_list, node,NodeName,'nodes')
    
    # List NamespaceBinding on Cluster
    if len(clusters) > 0:
       for cluster in clusters:
          ClusterName = AdminConfig.showAttribute(cluster, 'name')
          print "Retrieve NameSpaceBinding per cluster %s .. " % ClusterName 
          NameSpaceBinding_list = AdminConfig.list("NameSpaceBinding", cluster)
          listNameSpaceBinding(NameSpaceBinding_list, cluster,ClusterName,'clusters')
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

