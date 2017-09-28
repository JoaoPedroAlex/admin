
import os
#import platform
import java.io.File as f
import sys

print "Info V. 1.0"
from time import gmtime, strftime

def getResourcesPath():
    return  "%s/../resources" %(os.path.dirname(__file__))

def getCommonPath():
    return  "%s/../common" %(os.path.dirname(os.path.abspath(__file__)))

def getScriptsPath():
    return  "%s/../" %(os.path.dirname(os.path.abspath(__file__)))

def getInfoPath():
    return  "%s" %(os.path.dirname(os.path.abspath(__file__)))

def getInputPath():
    return  "%s/../../input" %(os.path.dirname(os.path.abspath(__file__)))

def getBinPath():
    return  "%s/../../bin" %(os.path.dirname(os.path.abspath(__file__)))

def printStatement(msg):
    tm =strftime("%d-%m-%Y %H.%M.%S",gmtime())
    print "[%s] %s" % (tm, msg)


