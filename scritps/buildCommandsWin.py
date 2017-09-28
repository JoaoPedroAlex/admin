# Authors: Joao Alexandre

# Version        Description
#
# 1.0.0          Starting version
# Import 
import sys 
import java 
import time
from string import replace


commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
infoPath = info.getInfoPath()
execfile("%s/%s" % (commonPath, "Utility.py"))

scriptName = "builCommands.py"
version = "1.0.0"

# Read input and target data file
print "Read input and target data file ..."
inputPath = info.getInputPath()
outputPath = "%s/commands.bat" % (info.getBinPath())
f = open(outputPath, "w")

inputPath = '%s/DS' % (inputPath)
#list files in directory
#it didn't work in Windows Platform
#fi = open(inputPath, "r")
#filenames = fi.readlines()
#fi.close()
#replace with
#isWindows = isWindows()
commands = []
for filename in os.listdir(inputPath):
#if len(filenames) > 0:
#      for filename in filenames:
#         filename = filename[:-1]
#         if isWindows: 
   commands.append("%%WAS_HOME%%\\bin\wsadmin.bat -lang jython -f %s\CreateDatasource.py %s\%s -javaoption -Dwsadmin.script.libraries=%s" % (resourcesPath,inputPath,filename,infoPath))
            #\bin\wsadmin.bat\" -lang jython -f "resourcesPath"\CreateDatasource.py "inputPath"/%s -javaoption -Dwsadmin.script.libraries="infoPath % (filename)
            #commands.append("%%WAS_HOME%%\"\bin\wsadmin.bat\" -lang jython -f "resourcesPath"\CreateDatasource.py "inputPath"/%s -javaoption -Dwsadmin.script.libraries="infoPath % (filename))
#         else:
#            commands.append("$WAS_HOME/bin/wsadmin.sh -lang jython -f %s/CreateDatasource.py %s/%s -javaoption -Dwsadmin.script.libraries=%s" % (resourcesPath,inputPath,filename,infoPath))

#inputPath = inputPath"/AS"
#fi = open(inputPath, "r")
#filenames = fi.readlines()
#fi.close()

#if len(filenames) > 0:
#      for filename in filenames:
#filename = filename[:-1]
#if isWindows(): 
#  commands.append("%%WAS_HOME%%\"\bin\wsadmin.bat\" -lang jython -f "resourcesPath"\CreateActivationSpecs.py "inputPath"\%s -javaoption -Dwsadmin.script.libraries="infoPath % (filename))
#else:
#  commands.append("$WAS_HOME/bin/wsadmin.sh -lang jython -f "resourcesPath"/CreateActivationSpecs.py "inputPath"/%s -javaoption -Dwsadmin.script.libraries="infoPath % (filename))

void = display(commands, f)
f.close()

