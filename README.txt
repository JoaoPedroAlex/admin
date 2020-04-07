Set variables in install.properties.bat, when executed in windows 
Set variables in was-config.properties 

In order to this works wsadmin command must execute with option: -javaoption -Dwsadmin.script.libraries=${scripts.dir}/info
In Windows that option didn't work because it needs to be between '', so I have to copy the directories scripts/info e scripts/common to WAS_HOME/scriptLibraries
In unix it is no need...






the scripts to define resources like createJDBCProviders, need to be invoked with parameter -Dwsadmin.script.libraries=${basedir.unix}/scripts/info between quotes.
 To be able to execute these using ant, I have copied the info and common directory to the C:\IBM\WebSphere\AppServer\scriptLibraries

Here is an example of the usage of this in the build.xml file:
<arg line="-username ${adminID} -password ${adminPasswd} -f ${basedir.unix}/scripts/resources/CreateActivationSpecs.py ${theFile} -lang jython -port ${soapPort} -conntype soap -javaoption -Dwsadmin.script.libraries=${basedir.unix}/scripts/info"/>
		
TODO: Investigate this better, find a solution ....

Changed the CreateDatasource.py to be ablr to define the following parameter:
mappingConfigAlias='DefaultPrincipalMapping'

code added:
    if len(mappingConfigAlias.strip()) > 0: 
           AdminConfig.create('MappingModule', datasource, '[[authDataAlias ' + authenticationAlias + '] [mappingConfigAlias ' + mappingConfigAlias + ']]')
    
Install resource adapter
create Connection factory

Problem:

     [exec] Traceback (innermost last):
     [exec]   File "<string>", line 14, in ?
     [exec]   File "C:\IBM\WebSphere\AppServer\scriptLibraries\info/../common/Utility.py", line 19,
in ?
     [exec]   File "C:\IBM\WebSphere\AppServer\scriptLibraries\info/../common/Utility.py", line 17,
in getCommonPath
     [exec] NameError: __file__

Solution:
change your codes as follows! it works for me. `

os.path.dirname(os.path.abspath("__file__"))

Problem:
     [exec] Traceback (innermost last):
     [exec]   File "<string>", line 14, in ?
     [exec]   File "C:\IBM\WebSphere\AppServer\scriptLibraries\info/../common/Utility.py", line 20,
in ?
     [exec] IOError: File not found - C:\Users\Administrator\IMEX\wsadminlib.py (The system cannot f
ind the file specified.)

Solution:
def getCommonPath():
    return  "%s/scripts/common" %(os.path.dirname(os.path.abspath("__file__")))
	
	properties.txt is a created when you choose the option to install an application.

TODO: how to increase the font size of <label>Add certificates to NodeDefaultTrustStore</label> in ant	

I have changed the wsadminlib.py in C:\IBM\WebSphere\AppServer\scriptLibraries\common, function parseargs which have changed the installapp and updateapp input parameter servers 
format from 'node1,server1,node2,server2' to 'node1:server1,node2:server2'

