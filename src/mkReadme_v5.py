#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 08:41:51 2020

@author: luciennemicallef, markusscheinert
"""

from scriptMK_v5 import ReadmeScript
from scriptMK_v5 import color
import scriptMK_v5 as mk

ReadmeC_ = ReadmeScript()#create an instance for class ReadmeScript()

scriptLoc=""
scriptLoc = ReadmeC_.checkScriptLocation()
if scriptLoc != None:
    ReadmeC_.exp = scriptLoc
else:
    ReadmeC_.exp=""
#MMS run : variable holding the experiment's name.
run=""

ReadmeC_.getNemoConfig()

color()
#
mk.hr()
mk.center("Technical Documentation")
mk.hr()
#
ReadmeC_.check_gitorsvn()
#
ReadmeC_.get_zGITNMSPC()
#
#    
ReadmeC_.check_prereq()
#
ans = mk.prep_note()
#
#call the main function

if(ans == 'y') and (ReadmeC_.exp != ""):
    #print("Exp 2 ", mk.exp)
    ReadmeC_.mainconfig() #if script is stored in a particular configuration
    
