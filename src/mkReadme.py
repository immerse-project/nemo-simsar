#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 08:41:51 2020

@author: luciennemicallef, markusscheinert
"""

import scriptMK as mk

scriptLoc=""
scriptLoc = mk.checkScriptLocation()
#print("script loc ", scriptLoc)
if scriptLoc != None:
    mk.exp = scriptLoc
else:
    mk.exp=""
#MMS run : variable holding the experiment's name.
run=""

mk.getNemoConfig()

mk.color()
#
mk.hr()
mk.center("Technical Details")
mk.hr()
#
mk.check_gitorsvn()
#
mk.get_zGITNMSPC()
#
#    #
mk.check_prereq()
#
ans = mk.prep_note()
#
#call the main function

if(ans == 'y') and (mk.exp == ""):
#    print("Exp 1 ", exp)
    mk.main() #if script is stored in the root

elif(ans == 'y') and (mk.exp != ""):
#    print("Exp 2 ", exp)
    mk.mainconfig() #if script is stored in a particular configuration
    
