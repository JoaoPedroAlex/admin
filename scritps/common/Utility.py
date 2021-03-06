# Authors: Sergio Stinchi

# Version  Changed by      			Description

# 1.3.0		Joao Pedro Alexandre	Add code to list also Microsoft datasources
# 1.2.0         					Modified def functions to check resources
# 1.1.0          					Add Definition getProviderType()
# 1.0.0          					Starting version
import os
import sys
from java.io import File



commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "wsadminlib.py"))

from java.util import Date
from java.lang import String as jString
from java.text import SimpleDateFormat
from java.util import Properties
from java.util import HashMap


#print (File(".").getCanonicalPath())


# Variables
scriptUtilityName = "Utility.py"
version = "1.3.0"

print "%s V%s" % (scriptUtilityName, version)

def isWindows(washome):
#	nodename = getNode(washome)
#	return getNodePlatformOS(nodename) == 'windows'
	if (washome.find(':') == 1): return True
	else: return False

#	print "platform: %s " % (os.getenv("windows"))
#	print "platform: %s " % (os.get_os_type)
#	return (os.get_os_type() == 'nt')
#	platform = os.name
#	if platform == 'nt': return True
# 	else: return False
    
   # return platform.system() == 'Windows'

def clearExit(text, status):
   if len(text): print text
   AdminConfig.reset()
   print "%s done" % scriptUtilityName
   sys.exit(status)
   return

def AdminConfigShowAttribute(obj, attrib):
        # print "<<AdminConfigShowAttribute>> get attribute value %s from %s"  %(attrib,obj)
        try:
                res = str(AdminConfig.showAttribute(obj, attrib))
                if res == 'None': res=''
        except:        
                # print "<<AdminConfigShowAttribute>> error getting value for %s from %s" % (attrib, obj)
                res = ''  
        return res

def wsadminToList(inStr):
        inStr = inStr.rstrip();
        outList = []
        if (len(inStr) > 0 and inStr[0] == '[' and inStr[-1] == ']'):
                tmpList = inStr[1:-1].split(" ")
        else:
                tmpList = inStr.split("\n")  # splits for Windows or Linux
        for item in tmpList:
                item = item.rstrip();  # removes any Windows "\r"
                if (len(item) > 0):
                      outList.append(item)
        return outList
# endDef
def save(hasChanges):
   if hasChanges == 1: 
      print "Save ..." 
      AdminConfig.save() 
      print "Save done" 
# end def
def syncEnv(hasChanges):
   if hasChanges == 1: 
      print "Save ..." 
      AdminConfig.save() 
      print "Save done" 
      print "Synchronization ..." 
      nodes = AdminControl.queryNames('type=NodeSync,*') 
      if len(nodes) > 0: 
         nodelist = nodes.splitlines()       
         for node in nodelist: 
            beg = node.find('node=') + 5 
            end = node.find(',', beg) 
            print "Synchronization for node \"" + node[beg:end] + "\" :",
            try: AdminControl.invoke(node, 'sync') 
            except: print "KO" 
            else: print "OK" 
   else: 
      print "No running nodeagents found" 
   print "Synchronization done" 
# end def

def checkScopeName(scopeName):
    print " Check scopeName ... for %s" % (scopeName)  
    scope = None 
    scopeid = None 
    nodeName = None 
    serverName = None 
    clusterName = None
    cell = AdminConfig.list('Cell') 
    nodes = AdminConfig.list('Node') 
    clusters = AdminConfig.list('ServerCluster') 
    servers = AdminConfig.list('Server') 
    if cell.find(scopeName + '(') != -1: 
       scope = 'Cell' 
       scopeid = cell 
       #print "Scope: %s - id: %s" % (scope, scopeid) 
    elif nodes.find(scopeName + '(') != -1: 
       scope = 'Node' 
       beg = nodes.find(scopeName + '(') 
       end = nodes.find(')', beg) + 1 
       scopeid = nodes[beg:end]
       nodeName = scopeName
       #print "Scope: %s - id: %s" % (scope, scopeid) 
    elif clusters.find(scopeName + '(') != -1: 
       scope = 'ServerCluster' 
       beg = clusters.find(scopeName + '(') 
       end = clusters.find(')', beg) + 1 
       scopeid = clusters[beg:end] 
       clusterName = scopeName
       #print "Scope: %s - id: %s" % (scope, scopeid) 
    elif servers.find(scopeName + '(') != -1: 
       scope = 'Server' 
       beg = servers.find(scopeName + '(') 
       end = servers.find(')', beg) + 1 
       scopeid = servers[beg:end] 
       #print "ScopeName %s  - Scope: %s - id: %s" % (scopeName, scope, scopeid) 
    elif scopeName.find(':') != -1: 
       scope = 'Server' 
       colon = scopeName.find(':') 
       nodeName = scopeName[:colon] 
       serverName = scopeName[colon + 1:] 
       scopeid = AdminConfig.getid('/Node:' + nodeName + '/Server:' + serverName + '/')
       if len(scopeid) == 0: 
          print "ERROR: %s not found" % (scopeName) 
          print "%s done" % (scriptUtilityName) 
          sys.exit(-1) 
       # print "Scope: %s - id: %s" % (scope, scopeid) 
    else: 
       print "ERROR: %s not found" % (scopeName) 
       print "%s done" % (scriptUtilityName) 
       sys.exit(-1) 
       
    #print "Check scope %s done" % (scopeName)
    #print "scope= %s " %(scope)
    #print "scopeid= %s " %(scopeid)
    #print "scopeName= %s " %(scopeName)
    #print "nodeName= %s " %(nodeName)
    #print "serverName= %s " %(serverName)
    #print "clusterName= %s " %(clusterName)
    return scope , scopeid, scopeName, nodeName, serverName, clusterName
    
#def checkIfJ2CAdminObjectExist(scopeid, resourceName, typeObject):
#   J2CAdminObjects = AdminTask.listSIBJMSQueues(scopeid)
#   if len(J2CAdminObjects) == 0: return None
#   for J2CAdminObject in J2CAdminObjects.splitlines():
#      name = AdminConfig.showAttribute(J2CAdminObject, 'name')
#      # print "name = %s - resourceName = %s  " % (name,resourceName) 
#      if name.find(resourceName) != -1:
#         return J2CAdminObject
#   return None   

def checkIfDestinationExist(resourceName, busName): 
   sibDestinations = AdminTask.listSIBDestinations('[-bus ' + busName + ' ]') 
   if len(sibDestinations) == 0: return None 
   for sibDestination in sibDestinations.splitlines():
      identifier = AdminConfig.showAttribute(sibDestination, 'identifier')
      if identifier.find(resourceName) != -1: 
         return sibDestination 
   return None       

#def checkIfResourceExist(scopeid, resourceName, typeObject):
#   try:
#      nameSpaceBinding = AdminConfig.list(typeObject, scopeid) 
#      if len(nameSpaceBinding) == 0: return None
#      if nameSpaceBinding.find(resourceName + '(') != -1:
#         beg = nameSpaceBinding.find(resourceName + '(')
#         end = nameSpaceBinding.find(')', beg) + 1
#         return nameSpaceBinding[beg:end]
#   except:
#      print "KO"
#      type, value, traceback = sys.exc_info()
#      print "ERROR: %s (%s)" % (str(value), type)
#      clearExit("Rollback and exit", -1)

#If the resource exist return id of resource , name of resources
def checkIfResourceExist(scopeid, resourceName, typeObject):
    #print "id = %s - Name = %s , typeObject %s " % (scopeid,resourceName, typeObject)
    resourceIds = AdminConfig.list(typeObject, scopeid) 
    if len(resourceIds) == 0: 
        return None ,None
    for resourceId in resourceIds.splitlines():
       #print "id = %s " % (resourceId)
       if resourceId.find(resourceName + '(') != -1:
          beg = resourceId.find(resourceName + '(')
          end = resourceId.find(')', beg) + 1
          #print "id = %s - Name = %s  " % (resourceId ,resourceId[beg:end]) 
          return resourceId , resourceId[beg:end]
       else:
          continue
    return None , None 
        
def getNodeNameForServer(ServerID):
   beg = ServerID.find('/nodes/') + len('/nodes/')
   end = ServerID.find('/', beg)
   out = ServerID[beg:end]    
   return  out

def getServerName(ServerID):
   #print "ServerID == %s " % (SeverID)
   beg = ServerID.find('/servers/') + len('/servers/')
   end = ServerID.find('|', beg)
   app = ServerID[beg:end]
   return app

def getScopeResources(nmsp_id):
   print "ID scope = %s " %(nmsp_id)
   beg = 0
   end = nmsp_id.find("(")
   nmSpace = nmsp_id[beg:end]
   name_cell = AdminConfig.showAttribute(AdminConfig.list('Cell'), 'name')
   #Was7Cell(cells/Was7Cell|cell.xml#Cell_1)
   #ORACLE_DS_NODE(cells/Was7Cell/nodes/was7Node01|resources.xml#DataSource_1412085327141)
   if nmsp_id.find('/servers/') != -1:
      nmsp_id.find('/nodes/')
      beg = nmsp_id.find('/nodes/') + 1
      end = nmsp_id.find('|', beg)
      out = nmsp_id[beg:end]    
      str = "%s:%s" % (out.split('/')[1], out.split('/')[3])
      # print " scope   %s = %s" % (nmSpace,str)
      return  str
   elif nmsp_id.find('/clusters/') != -1:
      beg = nmsp_id.find('/clusters/') + 1
      end = nmsp_id.find('|', beg)
      out = nmsp_id[beg:end]    
      scope = out.split('/')[0]
      name_scope = out.split('/')[1]
      str = "%s" % (name_scope)
      # print " scope   %s = %s" % (nmSpace,str)
      return str
   elif nmsp_id.find('/nodes/') != -1:
      beg = nmsp_id.find('/nodes/') + len('/nodes/')
      end = nmsp_id.find('|', beg)
      str = nmsp_id[beg:end]
      # print " scope   %s = %s" % (nmSpace,str)
      return str
   elif nmsp_id.find('(cells/') != -1:
      beg = nmsp_id.find('(cells/') + len('(cells/')
      end = nmsp_id.find('|', beg)
      str = nmsp_id[beg:end]
      # print " scope   %s = %s" % (nmSpace,str)
      return str
   else:       
       return None

def getStringScopeForId(scope, scopeid, scopeName, nodeName, serverName, clusterName):
   cell = AdminConfig.list('Cell')
   cellName = AdminConfig.showAttribute(cell, 'name')
   if scope == 'Server':
       str = "/Cell:%s/Node:%s/Server:%s" % (cellName, nodeName, serverName)
   elif scope == 'Node':
       str = "/Cell:%s/Node:%s" % (cellName, nodeName)
   elif scope == 'ServerCluster':
       str = "/Cell:%s/ServerCluster:%s" % (cellName, clusterName)
   else:
       str = "/Cell:%s" % (cellName)
   #print "getStringScopeForId() %s =%s " % (scopeName, str)
   return str
   
def getSIBBUSTarget(BusName):
   BusId = AdminConfig.getid('/SIBus:' + BusName + '/')
   busMembers = _splitlist(AdminConfig.showAttribute(BusId, 'busMembers'))
   for busMember in busMembers:
      scopeDestName = AdminConfig.showAttribute(busMember, 'cluster')
      #print "scopeDestName per cluster = %s " % (scopeDestName)
   if  scopeDestName == None or len(scopeDestName) == 0:
      scopeDestNameNode = AdminConfig.showAttribute(busMember, 'node')
      scopeDestNameServer = AdminConfig.showAttribute(busMember, 'server')
      scopeDestName = "%s:%s" % (scopeDestNameNode, scopeDestNameServer)
   return scopeDestName
def getProviderType(provider):
   esito=""
   providerType = AdminConfigShowAttribute(provider, 'providerType')
   if str(providerType).find('DB2') != -1:
      esito= "DB2"
   elif str(providerType).find('Oracle') != -1:
      esito= "Oracle"
   elif str(providerType).find('Derby') != -1:
      esito= "Derby"
   elif str(providerType).find('Microsoft') != -1:
      esito= "SQL Server"
   else:
      esito= None
   print "getProviderType %s == %s" %(provider,esito) 
   return esito

def getDataBaseType(provider):
   return getProviderType(provider)

def convertListToHashMap(J2EEProperySetList):
        # print "Properties for %s" % (obj)
        map = HashMap()
        if (len(J2EEProperySetList) == 0):return map
        propsetList = []
        # print "Propset= %s" % (propset) 
        try:
           for psItem in J2EEProperySetList:
              # print "psItem %s" % (psItem)
              propname = AdminConfigShowAttribute(psItem, "name")
              propvalue = AdminConfigShowAttribute(psItem, "value")
              # print "--------------"
              # print "propname " + str(propname)
              # print "propvalue " + str(propvalue)
              # print "--------------"
              map.put(propname, propvalue)
           # end for
        except:
           print "KO"
           type, value, traceback = sys.exc_info()
           print "ERROR: %s (%s)" % (str(value), type)
           return map
        return map

def display(lista, f1):
    # print "lista = %s" % (lista)
    for par in lista:
        print >> f1, par
    # print  riga
# end def

def checkIfIsNone(str):
   if str == None:
      return ''
   else:
      return str

def getTypeName(id):
   ObjStr = str(id)
   beg = id.find('#')  + 1
   end = id.find('_', beg)
   sType = id[beg:end]
   return sType
def checkIsNumber(value):
  try:
    int(value)
    return True
  except ValueError:
    return False

def checkIfIsServerTemplate(ScopeId):
     if ScopeId.find('/dynamicclusters/') != -1:
         return True
     else:
         return False


#def retrieveDsConfigurationParameter(ds):
#   str=""
#   configurationParameters=""
#   value=""
#   print "DS = %s" %(ds)
#   propsSet = AdminConfig.showAttribute(ds, 'propertySet')
#   resourceProperties = AdminConfig.showAttribute(propsSet, 'resourceProperties')[1:-1].split()
#   configurationParameters = " [ "
#   for rsp in resourceProperties:
#      name =  AdminConfig.showAttribute(rsp,'name')
#      value =  AdminConfig.showAttribute(rsp,'value')
#      if name in['URL','databaseName', 'serverName', 'portNumber', 'driverType']:
#         if str!="":
#            str += "\n"
#         str += "%s='%s'" %(name,value)
#      else:
#          configurationParameters += " ['%s','%s','%s']  " %(AdminConfig.showAttribute(rsp,'name'),AdminConfig.showAttribute(rsp,'type'),AdminConfig.showAttribute(rsp,'value')) 
#   configurationParameters += " ] "
#   print str
#   return str , configurationParameters   
   
def retrieveDsConfigurationParameter(ds):
   str=""
   configurationParameters=""
   value=""
   print "DS = %s" %(ds)
   propsSet = AdminConfig.showAttribute(ds, 'propertySet')
   resourceProperties = AdminConfig.showAttribute(propsSet, 'resourceProperties')[1:-1].split()
   configurationParameters = "[ "
   for rsp in resourceProperties:
      name =  AdminConfig.showAttribute(rsp,'name')
      value =  AdminConfig.showAttribute(rsp,'value')
      if len(configurationParameters)>2:
         configurationParameters +=","
      configurationParameters += " ['%s','%s','%s']  " %(AdminConfig.showAttribute(rsp,'name'),AdminConfig.showAttribute(rsp,'type'),AdminConfig.showAttribute(rsp,'value')) 
   configurationParameters += " ]"
   return str , configurationParameters   
   
def isObjectInScope(ComponentId,scopeName,scopeType):
    #CellDS(cells/Was7Cell|resources.xml#DataSource_1412328773120)
    #ORACLE_DS_NODE(cells/Was7Cell/nodes/was7Node01|resources.xml#DataSource_1412085327141)
    #ORACLE_DS_SERVER(cells/Was7Cell/nodes/was7Node01/servers/pressass_entrate|resources.xml#DataSource_1412090969325)
    #ClusterDs(cells/Was7Cell/clusters/cls|resources.xml#DataSource_1412329699248)
    index = ComponentId.find(scopeType + "/" + scopeName + "|")
    #print "index = %s " %(index)
    if index != -1:
       #print "Object %s is In Scope" %(ComponentId) 
       return True
    else:  
       #print "Scope %s  not valid" %(scopeName)
       return False
    
    
    
    
