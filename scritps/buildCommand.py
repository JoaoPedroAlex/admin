#! /usr/bin/python
# Authors: Joao Alexandre

# Version        Description
#
# 1.0.0          Starting version
# Import 
import sys 
import java 
import time
from string import replace

global commonPath
commonPath = "E:\jscripts"
execfile("%s/%s" % (commonPath, "Utility.py"))

scriptName = "builCommands.py"
version = "1.0.0"

# Command Line
argc = len(sys.argv)
if argc != 2:
   print "Usage: %s <path input file> <output file> " % (scriptName)
   sys.exit(-1)

# Read input and target data file
print "Read input and target data file ..."
inputPath = sys.argv[0]
outputPath = sys.argv[1]

fi = open(inputPath, "r")
filenames = fi.readlines()
fi.close()
f = open(outputPath, "w")
commands = []
if len(filenames) > 0:
      for filename in filenames:
	commands.append("/opt/IBM/was/WebSphere/AppServer/profiles/DCDmgr/bin/wsadmin.sh -lang jython -f /opt/IBM/was/setup/scripts/resources/CreateConnectionFactory.py /opt/IBM/was/setup/input/CF/%s -javaoption -Dwsadmin.script.libraries=/opt/IBM/was/setup/scripts/info" % (filename))
      void = display(commands, f)
f.close()

