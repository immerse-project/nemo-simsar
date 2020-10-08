#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 08 13:07:20 2020

@author: luciennemicallef, markusscheinert
"""

import git
import os
#from os import path
import svn.local
import re
from jinja2 import Template
import pycurl
import wget
import subprocess
import pathlib
import textwrap
import glob
import netCDF4 as nc
import configparser

################ variables ########################

DS=False
LNGIT=False
LNSVN=False
CURRCONFIG=False
zGITUSER=""
zPAGE=""
zPAGESRV=""
rowsLst = [] #list to store all values
rowsLst2 = [] #list to remove empty tuples - this will be passed on to markdown template
release3=False
release4=False

################ end variables ########################


def getNemoConfig():
    '''This function will look for the directory 'NEMOGCM/CONFIG' for release 3 and 'cfgs' for release 4
    anywhere in the system'''
    global release3, release4
    #MMS:{
    #rootPath = pathlib.Path().absolute()
    #fname = []
    #configPath=""
    #for root,d_names,f_names in os.walk(rootPath):
    	#for f in d_names:
    		#fname.append(os.path.join(root, f))
    #for i in fname:
        #if "NEMOGCM/CONFIG" in i:
            #configPath = i
            #release3=True
            ##if this is True, the script is being run as a release 3
            #break
        #elif "cfgs" in i:
            #configPath = i
            #release4=True
            ##if this is True, the script is being run as a release 4
            #break
            
    #path = configPath
    ##if release is 4 remove the last two folders since the file structure is different in rel3 and rel4
    #if ((release3 == True) or (release4 == True)) and (scriptLoc != None):
        #pathSplit = os.path.dirname(path)
        #pathUpdated, tail = os.path.split(pathSplit)        
        #return pathUpdated
    #else:
        #return path

    rootPath = os.getcwd()
    if "/CONFIG/" in rootPath:
        release3=True
        configPath = ''.join(rootPath.partition("CONFIG")[:2])
    elif "/cfgs/" in rootPath:
        release4=True
        configPath = ''.join(rootPath.partition("cfgs")[:2])

    return configPath
        
    #:MMS}
    


def check_EXPref():
    '''This function will check whether the current location contains, EXP00 and EXPREF folder'''    
    path = os.getcwd()
    expRef = False
    
    #{MMS:
    #for root, directories, files in os.walk(path):
        #for folder in directories:
            ##release 3
            #if "EXP00" in folder:
                #expRef = True
                #break
            ##release 4
            #elif "EXPREF" in folder:
                #expRef = True
                #break
    (_, _, files) = next(os.walk(path))
    if 'namelist_cfg' in files:
        expRef = True
    #:MMS}
    return expRef



def main():
     '''This function will be called if the script is stored in the root'''
     check_inputDef_exists()
     #check if input.def is part of this directory
     if check_inputDef_exists() == True:
        exp = chooseConfigFolder()
        #print(ask_exp00())
        #MMS:{
        #if ask_exp00(exp) == True:
            #template()
        #else:
            #print("Exiting..Please start again")
        template()
        #:MMS}
     else:
        print("Input.def file does not exist, create this file to be able to proceed")
        
def mainconfig():
     '''This function will be called if the script is initially saved in one of the configuration folders'''
     check_inputDef_exists()
     #check if input.def is part of this directory
     if check_inputDef_exists() == True:
        if ask_exp00(exp) == True:
            template()
        else:
            print("Exiting..Please start again")
     else:
        print("Input.def file does not exist, create this file to be able to proceed")
        
    
def getAllConfigFolders():
    '''This function will return a list of configurations, and eventually user will choose 
        which configuration s/he would like to work with:
        (e.g. AMM12, ORCA2_LIM_CFC_C14b, GYRE, ORCA025.L46.LIM2vp.CORE.XIOS1, ORCA2_LIM etc..
        Display only the configurations that include EXP00 folder'''

    configFolders=[]
    listWithAllDir = []
    listOnlyExp00=[]

    configPath = getNemoConfig()
    #print("Config path" , configPath)
    
    for r, d, f in os.walk(configPath):
        for directory in d:
            if "EXP00" in d: #release3
                listWithAllDir.append(os.path.join(r,directory))
            elif "EXPREF" in d: #release 4
                listWithAllDir.append(os.path.join(r,directory))
                
            
    for i in listWithAllDir:
       if "EXP00" in i:
           #remove the EXP00 
           listOnlyExp00.append(i)
       elif "EXPREF" in i:
           #remove the EXPREF 
           listOnlyExp00.append(i)
           
       
    for c in listOnlyExp00:
        last = c.split('/')
        configFolders.append(last[-2])
   
    #sort configFolders
    configFolders.sort()
    return configFolders

def chooseConfigFolder():
    '''This function will ask the user to select one configuration from the list generated from getAllConfigFolders.
    The chosen config is stored in a global variable called exp which will be used throughout the script'''
    #MMS:{
    #'''This function will ask the user to select one configuration from the list generated from getAllConfigFolders.
    #The chosen config is stored in a global variable called exp which will be used throughout the script'''
    #valid = False
    global exp
    #configList = []
    #print("\n\nConfig List: \n")
    #for i in getAllConfigFolders():
        #configList.append(i)
        #print(i)
    #while valid == False:
        #exp = input("\n Choose one of the above configurations : \n\n")
        #if exp in configList:
            #valid = True
            #return exp
        #else:
            #print("Invalid entry, input has to match exactly (including capital letters)")
    path = os.getcwd()
    exp = path.split("/")[-2]
    run = path.split("/")[-1]
    #:MMS}
            
def checkScriptLocation():
    '''The purpose of this function is to check whether the script is being run from a particular configuration'''
    path2 = os.getcwd()
    configName = os.path.basename(path2) 
    #print("This script is saved in ", configName)
    for x in getAllConfigFolders():
        if x == configName:
            global CURRCONFIG
            CURRCONFIG = True
            return x
                   
def fillenv():          
    '''This function returns variables which will be used to create the readme file'''
    global _CONFNAME_
    _CONFNAME_= get_confname()                    
    global _EXPNAME_
    _EXPNAME_= get_expname()
    global _CONTACT_
    _CONTACT_= get_username() + " - " + get_useremail() 
    global _PURPOSE_
    _PURPOSE_=get_purpose()
    global _CURREPO_ 
    _CURREPO_=get_currepo()
    global _NEMOREPO_
    _NEMOREPO_=get_nemorepo()
    global _NEMOREVISION_
    _NEMOREVISION_=get_nemorevision()
    global _NEMOBRANCH_
    _NEMOBRANCH_=get_branch()
    global _COMPONENTS_
    _COMPONENTS_ = get_components()
    global _REFCONFIG_
    _REFCONFIG_=get_refconfig()
    global _CPPKEYS_
    _CPPKEYS_=get_cppkeys() 
    global _RESOLUTION_
    _RESOLUTION_= get_resolution()
    global _GRID_
    _GRID_ = get_hgridtype() + ", " + get_vgridtype()
    global _HGRIDPT_
    _HGRIDPT_=get_hgridpt()
    global _VGRIDPTZ_
    _VGRIDPTZ_=get_vgridpt()
    global _ATMOS_
    _ATMOS_=get_atmos()
    global _OCEANRDT_
    _OCEANRDT_ =  get_oceanrdt()
    global _NESTNUMBER_
    _NESTNUMBER_= get_nestnumber()
    global _PASSIVTRACERS_
    _PASSIVTRACERS_ = get_passivetracers()
    
    global _zGITSERVER_
    _zGITSERVER_ = get_zGITSERVER()
    global _zGITNMSPC_
    _zGITNMSPC_ = get_zGITNMSPC()
    global _zPAGE_
    _zPAGE_ = get_zPAGESRV()
    
 
class color():
    '''This class stores a list of colours and font styles'''
    global RED
    RED ='\033[31m'
    global GREEN
    GREEN ='\033[32m'
    global YELLOW
    YELLOW ='\033[93m'
    global BLUE
    BLUE ='\033[34m'
    global PURPLE
    PURPLE ='\033[35m'
    global CYAN
    CYAN ='\033[36m'
    global WHITE
    WHITE ='\033[37m'
    global BLACK
    BLACK ='\033[30m'
            
    #set style in python
    global NORMAL
    NORMAL ='\033[0m'
    global ULINE
    ULINE ='\033[04m'
    global BOLD
    BOLD ='\033[1m'
    global DIM
    DIM ='\033[2m'
    
def errmsg(msg):           
    ''' Displays an error message in RED and reset text colour - Message will be passed as a parameter'''
    print(RED + '\n ERROR: ' + msg + '\n\n' + NORMAL)
    
def warnmsg(msg):
    ''' Displays an error message in YELLOW and reset text colour - Message will be passed as a parameter'''           
    print(YELLOW + '\n WARNING: ' + msg + '\n\n' + NORMAL)
    
def sucssmsg(msg):        
    ''' Displays an error message in GREEN and reset text colour - Message will be passed as a parameter'''
    print(GREEN + '\n SUCCESS: ' + msg + '\n\n' + NORMAL) 
    
def indent(text):
    '''Indents text to the right'''            
    text = textwrap.indent(text, ' ' * 4)[4 - 1:]
    print(text)
        
def center(text):            
    '''Centers the text to the midddle of the screen'''
    command = ['tput', 'cols']
    width = int(subprocess.check_output(command))
    print (text.center(width), "\n") 
    
def hr():
    '''displays a list of * across the page and moves cursor to next line'''
    command = ['tput', 'cols']
    width = int(subprocess.check_output(command))               
    for i in range(width): 
        {
         print("*", end="")
        }
    print("\n")

def trim(text):
    '''If any white spaces are present at the end of a line, the purpose of this function is to  remove them'''               
    text = text.strip()
    return text
 
def ask_exp00(exp):
   '''exp is the configuration name'''
   '''The purpose of this function is to show all directories for the chosen configuration '''
      
   print("\nChosen configuration is : ",exp)
 
   #list to store all the directories inside this configuration
   listWithAllDir = []

   configPath = getNemoConfig() + "/"+exp
   #print("Config path" , configPath)
   print("\nDirectories for : ", exp)
   for r, d, f in os.walk(configPath):
      for directory in d:
         listWithAllDir.append(directory)
        
   #sort list
   listWithAllDir.sort()
   for i in listWithAllDir:
       print(i)
 
   choice = input("\n --> Are you sure that this is the configuration you would like to work with? Proceed with [Y] or [N] \n\n")
   choice = choice.lower()
   if choice == 'y':
       return True
   else:
       return False
      
   
def check_gitorsvn():
    '''The purpose of this function is to check whether the current script is stored as a git repo or as an svn repo'''
    '''if LNGIT is True - the script is stored as a git repo'''
    '''if LNSVN is True - the script is stored as an svn svn repo'''
    global repo

    try:
        #MMS repo = git.Repo(".", search_parent_directories=True)
        repo = git.Repo("../../", search_parent_directories=True)
    except git.InvalidGitRepositoryError:
        print(BLUE + "This is not a git repo \n" + NORMAL)
        
    else:
        print(BLUE + "This is a Git Repo" + NORMAL)
        global LNGIT
        LNGIT=True
        
    if (LNGIT == False):
        try:
           #repo = subprocess.check_output("svn info | awk '/^Kind:/ {print $2}'", shell=True).strip()
           repo = subprocess.check_output("LC_ALL=C svn info | awk '/^Kind:/ {print $2}'", shell=True).strip()
        except svn.exception.SvnException:
            print(BLUE + "This is not an svn repo \n" + NORMAL)
        except OSError as e:
            print("Error - ", e)
        else:
            print(BLUE + "This is an SVN Repo" + NORMAL)
            global LNSVN
            LNSVN=True
            
    
def get_confname():
    '''Returns the configuration name which is the variable stored as 'exp'  '''
    print("\n --> What is the name you want to use for publishing this configuration ? Our first guess is, that it's the configuration name in the current path. Accept with [ENTER] or modify accordingly:\n\n")  
    currentDirectory = os.getcwd()
    confName = os.path.basename(currentDirectory)
    pathSplit = currentDirectory.split('/')

    print(PURPLE+"Configuration's name: "+exp+""+NORMAL)#returns the chosen configuration by the use
    return exp
    
def get_expname():
    '''Returns the name of the current experiment folder'''
    global run
    #print("\n --> Control print of the current Experiment name (current folder):\n\n")
    currentDirectory = os.getcwd()
    run = os.path.basename(currentDirectory)
    
    print(PURPLE+"Experiment's name: "+run+""+NORMAL)
    return run

def get_username():
    '''This function returns the username, if available in the config file '''
        
    if(LNGIT == True):
        try:
            repo = git.Repo(".", search_parent_directories=True)
            print("\n --> What is your full name? We try to get it from git. Accept with [ENTER] or modify accordingly: \n\n")
            reader = repo.config_reader()
            default = reader.get_value('user','name')
            output = PURPLE + "User's Full Name :" + default + NORMAL
        #    return output
            print(output)
            return default
        except:
            try:
                choice = input("Config file does not include the user name, please amend accordingly in .git > config. Proceed with [ENTER] to continue with 'Unknown' or abort with CTRL-C: ")
            except KeyboardInterrupt:
                print("You pressed Ctrl+C!")
            finally:
                return "Unknown"
    else:
        pass
    
    if(LNSVN == True):
        try:
            username = input("\n --> What is your name? Enter your full name (temporarily) \n\n")    
            return username
        except KeyboardInterrupt:
            print("Exit..")
    

def get_useremail():      
     '''This function returns the user email, if available in the config file '''
     if(LNGIT == True):
         try:
             repo = git.Repo(".", search_parent_directories=True)
             print("\n --> What is your email address? We try to get it from git. Accept with [ENTER] or modify accordingly: \n\n")
             reader = repo.config_reader()
             default = reader.get_value('user','email')
             output = PURPLE + "User's email :" + default + NORMAL
             print(output)
             return default
             
         except:
            try:
                choice = input("Config file does not include the email address, please amend accordingly in .git > config. Proceed with [ENTER] to continue with 'Unknown' or abort with CTRL-C: ")
            except KeyboardInterrupt:
                print("You pressed Ctrl+C!")
            finally:
                return "Unknown"
     else:
        pass
    
     if(LNSVN == True):
        try: 
            email = input("\n --> Enter your email address (temporarily) or press [Ctrl-C] to exit and update through git-init \n\n")    
            return email
        except KeyboardInterrupt:
            print("Exit.. ")
    
def get_purpose():
    '''This function creates a text file to store the purpose of the readme file or reads the existing text file '''
    #MMS:{
    #pathS = pathlib.Path().absolute()
    
    #if (LNGIT==True) and (CURRCONFIG==False):
        #dirName = str(pathS) + "/CONFIG/" + exp + "/.includes"
    #elif (LNSVN==True) and (CURRCONFIG==False) and (release3 == True):
        #dirName = str(pathS) + "/NEMOGCM/CONFIG/" + exp  + "/.includes"
    #elif (LNSVN==True) and (CURRCONFIG==False) and (release4 == True):
        #dirName = str(pathS) + "/cfgs/" + exp + "/.includes"
    ##if current script is stored in one of the configurations
    #elif (CURRCONFIG == True):
        #dirName = str(pathS) + "/.includes"
    dirName = "./.includes"
    #:MMS}
    
    try:
        # Create target Directory
        os.mkdir(dirName)
        purpose = input("\n\n --> What's the purpose of this configuration?:\n")
        f = open(dirName + "/.recall_purpose.txt", "w")
        f.write(purpose)
        f = open(dirName + "/.recall_purpose.txt", "r")
        purpose = f.read()
        print(PURPLE+purpose+NORMAL)
        return(purpose)
        
    #if file already exists, read the contents and provide an option for modification (overwritten)    
    except FileExistsError:
        f = open(dirName + "/.recall_purpose.txt", "r")
        #ask if content is as expected
        print("\n\n --> What's the purpose of this configuration? Trying to remember last answer")
        purpose = f.read()
        print(PURPLE+purpose+NORMAL)
        
        choice = input("Accept with [ENTER] or modify accordingly (press [M] to modify): ")
        choice = choice.lower()
        if choice == 'm':
            purpose = input("Enter a new purpose, this will be overwritten: ")
            f = open(dirName + "/.recall_purpose.txt", "w")
            f.write(purpose)
            f = open(dirName + "/.recall_purpose.txt", "r")
            purpose = f.read()
            print(PURPLE+purpose+NORMAL)
            return(purpose)
        else:
            return(purpose)
    
        f.close()
        
    else:
        print("Unable to create this file, check admin rights")

def get_nemoGit():
    '''This function will search for the git file '''
    global nemoGitRepo
    pathSplit=""
    #find Nemo/.git
    proc = subprocess.check_output(["locate", "-r", "\.git$"])
    proc = str(proc)
    
    pathSplit = proc.split("\\n")
    
    for p in pathSplit:
        if "/NEMOGCM/.git" in p:
            nemoGitRepo=p
    
    return nemoGitRepo



def get_currepo():
    '''The purpose of this function is to display the actual repo from were NEMO was cloned'''
    print("\n --> Are we in a git/svn working tree? And from which remote repository was NEMOGCM cloned? Try to get it from git/svn. Accept with [ENTER]:\n")
    
    default=""
    revision=""
    
    if(LNGIT==True):
        try:
            repo = git.Repo(".", search_parent_directories=True)
            remoteLocation = repo.remote("origin").url
            default = remoteLocation
            
            if(default != "") & (LNGIT == True):
                print(PURPLE + "This is a GIT Repo " + NORMAL)
                print(PURPLE + "Actual Repository = "  + default + "" + NORMAL)
                return default
        
        except git.InvalidGitRepositoryError:
            print(PURPLE + "Not connected to GIT" + NORMAL)
    else: 
        pass
                
    if(LNSVN == True):
        try:
            #MMS default = subprocess.check_output("svn info | awk '/^URL:/ {print $2}'", shell=True).strip()
            default = subprocess.check_output("LC_ALL=C svn info --show-item url", shell=True).strip()
            revision = subprocess.check_output("LC_ALL=C svn info --show-item revision", shell=True).strip().decode().replace("'", "")
            #convert to string
            default = str(default)
            default = default.replace("'", "")
            if revision == "":
                print(RED + "SVN repository found, but current directory has not been committed" + NORMAL)
            elif(default != "") & (LNSVN == True) & (revision != ""):
                print(PURPLE + "This is an SVN Repo " + NORMAL)
                print(PURPLE + "Actual Repository = " + str(default[1:]) +  NORMAL)
                return default[1:]
            else:
                print(RED + "Not connected to SVN" + NORMAL) 
        except svn.exception.SvnException:
            print("This is not a working copy of SVN - Not connected to SVN")
        
    else:
        pass


def get_nemorepo():
    '''This function displays the URL of the repository the NEMO was installed from '''
    print("\n\n\n --> What is the URL of the repository you installed NEMO from? Try to get it from git/svn. Accept with [ENTER]:")    
    if(LNGIT==True):
        getIndexHash=""
        #command = '--grep="jussieu" --pretty=oneline --abbrev-commit --reverse | cut -d ' ' -f 3 |head -n 1'
        proc = subprocess.check_output(["git", "log", "--pretty=oneline", "--abbrev-commit", "--reverse"])
        proc = str(proc)
        getSvnIDText = proc.find('http')
        getIndexHash = proc.find('@')
        getUrl = proc[getSvnIDText:getIndexHash]
        print(PURPLE + ""+ getUrl + "" + NORMAL)
        return(getUrl)
    
    if(LNSVN==True):
        #command = '--grep="jussieu" --pretty=oneline --abbrev-commit --reverse | cut -d ' ' -f 3 |head -n 1'
        #MMS getURLsvn = subprocess.check_output("svn info | awk '/^URL:/ {print $2}'", shell=True).strip()
        getURLsvn = subprocess.check_output("LC_ALL=C svn info --show-item url $(LC_ALL=C svn info --show-item wc-root)", shell=True).strip()
        getURLsvn = str(getURLsvn)
        getURLsvn = getURLsvn.replace("'", "")
        print(PURPLE + ""+ str(getURLsvn[1:]) + "" + NORMAL)
        return(getURLsvn[1:])

   
def get_nemorevision():
    '''This function will display the revision number for the current NEMO version '''
    print("\n\n\n --> What is the NEMO revision you're currently using? Try to get it from git/svn history. Accept with [ENTER]:")
    if(LNGIT == True):
        try:
            proc = subprocess.check_output(["git", "log", "--pretty=oneline", "--abbrev-commit", "--reverse"])
            proc = str(proc)
            getSvnIDText = proc.find('http')
            getIndexHash = proc.find('#')
            nemoRev1 = proc[getSvnIDText:getIndexHash]
            getAT = nemoRev1.find('@')
            getspace = nemoRev1.find(' ')
            nemoRev2 = nemoRev1[getAT+1:getspace]
            print(PURPLE + nemoRev2 + NORMAL)
            return(nemoRev2)
        except git.InvalidGitRepositoryError:
            print(PURPLE + "Not connected to GIT" + NORMAL)
        except OSError as e:
            print("Error - ", e)
    
    if(LNSVN==True):
        try:
            #MMS nemoRev = subprocess.check_output("svn info | awk '/^Revision:/ {print $2}'", shell=True).strip()
            nemoRev = subprocess.check_output("LC_ALL=C svn info --show-item revision $(LC_ALL=C svn info --show-item wc-root)", shell=True).strip()
            nemoRev = str(nemoRev)
            nemoRev = nemoRev.replace("'", "")
            print(PURPLE + str(nemoRev[1:]) + NORMAL)
            return(nemoRev[1:])
        except svn.exception.SvnException:
            print("This is not an svn repo \n")
            
    
def get_branch():
    '''This function will return the branch number for this repo'''
    print("\n")
    print("--> Which branch are you using? Try to get it from git/svn. Accept with [ENTER]: ")
    if (LNGIT==True):
        repo = git.Repo(".", search_parent_directories=True)
        default = repo.active_branch
        print(PURPLE + str(default)+NORMAL)
        return default
    #else:
        #print ("LNGIT is false")
    
    if (LNSVN==True):
        #MMS getBranchInfo = subprocess.check_output("svn info | awk '/^URL:/ {print $2}'", shell=True).strip()
        getBranchInfo = subprocess.check_output("LC_ALL=C svn info --show-item url $(LC_ALL=C svn info --show-item wc-root)", shell=True).strip()
        getBranch = str(getBranchInfo)
        branchSplit = getBranch.split('/')
        #MMS branchSplit = getBranch.split('NEMO')
        #Get the last part of the string
        getBranch = branchSplit[-1]
        #MMS getBranch = branchSplit[1]
        getBranch  = getBranch.replace("'","")
        print(PURPLE + str(getBranch)+NORMAL)
        return getBranch
    #else:
        #print ("LNSVN is false")
        


def get_components():
    '''This function returns the NEMO components for this repo from cfg.txt or ref_cfg.txt'''
    cfgPath=""
    cfgPath2=""
    componentsLst=[]
    findExactComponent=[]
    componentsLst.append('\n')
    print("\n --> What NEMO components are we using? Try to get a comma-separated list from cfg.txt (or ref_cfgs.txt or work_cfgs.txt). Accept with [ENTER]: \n")
    #get file path for /cfg.txt
    currentDirectory = getNemoConfig() 
    confName = os.path.basename(currentDirectory)
    
    #MMS:{
    if release3 == True:
        #cfgPath = open(getNemoConfig() + "/cfg.txt", "r")
        cfgPath = open("../../cfg.txt", "r")
    elif release4 == True:
        #cfgPath = open(getNemoConfig() + "/ref_cfgs.txt", "r")
        cfgPath = open("../../ref_cfgs.txt", "r")
        cfgPath2 = open("../../work_cfgs.txt", "r")
    #:MMS}

    for i in cfgPath:
        if exp in i:
            componentsLst.append(i.strip())
    #MMS:{
    if cfgPath2:
        for i in cfgPath2:
            if exp in i:
                componentsLst.append(i.strip())
    #:MMS}
    #go through the list to check for multiplies
    if(len(componentsLst) == 1):
        #print(cfgNameLists)
        output = componentsLst
        
    else:
        #add each item to the list
        for i in range(len(componentsLst)):
            findExactComponent.append(componentsLst[i])

        #Search through each item for the exact configuration name
        for item in findExactComponent:
            #MMS:{
            #pathSplit = item.split(' ')
            if item.split(' ')[0] == exp:
                #Get the first element from the last
                #output = str(pathSplit[0])
                output = ', '.join(item.split(' ')[2:])
            #:MMS}
    #MMS:{
    comp = ''.join([str(elem) for elem in output])
    f = open("../exp_cfg.txt", "w")
    f.write("{}  {}".format(exp,comp.replace(',','')))
    f.close
    
    #print(PURPLE + ''.join([str(elem) for elem in output]) + NORMAL)
    #return ''.join([str(elem) for elem in output])
    print(PURPLE + comp + NORMAL)
    return comp
    #:MMS}


def get_refconfig():
    '''This function asks for user input to return the reference configuration for a particular configuration. This may also be left blank '''
    zrefconfname=""
    zrefconfurl=""
    zrefconfname = input("--> Name: If there is a reference configuration this particular configuration is based on, please type the name. Otherwise leave it blank by typing [ENTER].\n")
    zrefconfurl = input("--> URL: If there is a reference configuration this particular configuration is based on, please type the URL. Otherwise leave it blank by typing [ENTER].\n")
    return zrefconfname + " - " + zrefconfurl


def get_cppkeys():
     '''This function searches for .fcm file and extracts the cpp keys'''
     lastElement=""
     cppList = []
     cppList2 = []
     findExactCPP = []
     output = ""
     matchPath = ""
     multiples = False
     path = getNemoConfig()
     found = False

#MMS:{    
     #for (dirname, dirs, files) in os.walk(path):
##        for (dirname, dirs, files) in os.walk('.'):
      #for filename in files:
           #if exp in filename:
               #if filename.endswith('.fcm') :
                   ##ADD filename to list
                   #cppList.append(filename)
                   #if len(cppList) == 1:
                       #thefile = os.path.join(dirname,filename)
                       ##open file and read contents
                       #f = open(thefile, "r")
                       #cppkeysContents = f.read()
                       #f.close()
                   #else:
                       ##multiples is used when the config file appears more than once, e.g. ORCA2_LIM
                       #multiples = True
                       
     ##add each item to the list
     #if(multiples == True):
           #for i in range(len(cppList)):
               #findExactCPP.append(cppList[i])
                   ##Search through each item for the exact CPP key
               #for item in findExactCPP:
                   ##item e.g. cpp_GYRE_PISCES.fcm, split by first _ and .
                  #underscoreIndex = item.find("_")
                  #dotIndex = item.find(".")
                  #res = item[underscoreIndex+1:dotIndex] 
                  #if res == exp:
                      #found = True
                      #break

     #if(found == True):
           #matchPath = os.path.join(path, res, item)
           ##print(matchPath)
           #x = open(matchPath, "r")
           #cppkeysContents = x.read()
           #x.close()
           
     matchPath = glob.glob('../cpp_'+exp+'.fcm')
     try:
         x = open(''.join(matchPath), "r")
         cppkeysContents = x.read()
         x.close()
     except:
         print('Could not open'+'../cpp_'+exp+'.fcm')
         raise
#:MMS}
            
     #remove bld::tool::fppkeys by replacing this text empty text
     #sample: bld::tool::fppkeys key_diaeiv key_dynldf_c2d
     content = cppkeysContents.replace('\n', ' ')
     content = content.replace('bld::tool::fppkeys ', '')
     return ''.join(str(content))
         
def getNameLists():
    ''' This function searches for namelist_cfg file and extracts the namelist path for the chosen configuration'''    
    #to retrieve only the cfg of the chosen configuration
    cfgNameLists = []
    findExactNameList = []
    output = ""
    
    #MMS:{        
    #path2 = getNemoConfig()
    #for (dirname, dirs, files) in os.walk(path2):
    ##for (dirname, dirs, files) in os.walk('.'):
        #for filename in files:
            #if filename.startswith('1_namelist_cfg'):
                #pass #ignore
            #elif 'namelist_cfg' in filename :
                #thefile = os.path.join(dirname,filename)
                #if exp in thefile:
                    #cfgNameLists.append(thefile)
                    
    ##go through the list to check for entries containing part of the chosen name
    #if(len(cfgNameLists) == 1):
        ##print(cfgNameLists)
        #output = cfgNameLists
        
    #else:
        ##add each item to the list
        #for i in range(len(cfgNameLists)):
            #findExactNameList.append(cfgNameLists[i])
        ##Search through each item for the exact configuration name
        #for item in findExactNameList:
            ##for i in item:
                #pathSplit = item.split('/')
                ##Get the third element from the last
                #if exp == pathSplit[-3]:
                    ##print(item)
                    #output = item #return full path
        
    ##convert list to str
    #return ''.join([str(elem) for elem in output])
    
    ##MMS-----------
    
    return './namelist_cfg'

    #:MMS}
        
def get_resolution():
    '''This function will return the value corresponding to the resolution 
    of the horizontal grid from namelist_cfg file. Returns unknown if value is not available '''
    
    stringToMatch = 'namcfg'
    defaultK = ""
    output = 0
     #get list of namelists
    allCFG = getNameLists()
    print("+++get_resolution: allCFG=", end='')
    print(allCFG)
    #remove empty spaces
    allCFG = allCFG.replace(" ", "")

    print("\n --> The resolution of the horizontal grid. Accept with [ENTER]: \n\n")
    
    #MMS:{
    if release3:
    
        f = open(allCFG, "r")
        print("all CFG is ", allCFG)
        for line in f:
            #find the section namcfg
            if stringToMatch in line: 
                #print(line)
                for line in f:
                    if "jp_cfg" in line:
                        defaultK = line
                        break
        output=0
        repl_str = re.compile('^\d+$')
        line = defaultK.split()
        for word in line:
                match = re.search(repl_str, word)
                if match:
                    output = float(match.group())
                    #print(BOLD + "Vertical Grid Points (K): " + NORMAL + "" + str(output))

    elif release4:
        f = open(allCFG, "r")
        for line in f:
            #find the section namcfg
            if stringToMatch in line: 
                #print(line)
                for line in f:
                    if "cn_domcfg" in line:
                        defaultK = line
        f.close()

        domcfg_fname = defaultK.split('=')[1].lstrip().split(' ')[0].replace('"', '') + '.nc'
        
        try:
            ds = nc.Dataset(domcfg_fname)
            # NC variable 'ORCA_index' in domaincfg = jp_cfg in old namelist_cfg
            output = ds['ORCA_index'][:]
        except FileNotFoundError:
            print("could not read from " + domcfg_fname)
        
    #print(defaultK)
    #extract digits only from defaultK
    
   
    print(PURPLE + str(output) + NORMAL)
    return str(output)
    


    
def get_hgridtype():
    '''This function will return the value corresponding to the horizontal grid type from namelist_cfg file. Returns unknown if value is not available'''
    stringToMatch = 'namcfg'
    matchedLine = ''
    endStringToMatch = "/"
    endStringToMatch2 = "cp_cfg"
    output = ""
    #get list of namelists
    allCFG = getNameLists()
    #remove empty spaces
    allCFG = allCFG.replace(" ", "")
    result = ""
    #default = ""

    print("\n --> Horizontal grid type, e.g. ORCA for a global tri-polar grid. Accept our guess with [ENTER]:\n\n")
    
    #MMS:{
    if release3:

        #go through the list of files with namelist_cfg
        #for line in allCFG:
            #for each file read..
        f = open(allCFG, "r")
        #print("File Name ", line)
        for line in f:
            if stringToMatch in line:
                matchedLine = line
                #print("Matched Line ", matchedLine)             
                for line in f:
                    output = line
                    result = result + line
                    #print("Output ", line)
                    #outputS = BOLD + "Horizontal Grid Type: "+NORMAL+output
                    #print(outputS)
                    #hGridType.append(outputS)
                    #continue printing until line matches "/"
                    #if (line.startswith("/")):
                    if endStringToMatch2 in line:
                        break
        
        x = result.split("!")
        #remove the dashed line
        newX = ""
        for i in x[1]:
            newX = newX + i.replace('-','')
        
        #return only the value in the "" and do not print cp_cfg
        _index = newX.find("=")
        default = newX[_index+1:] #retrieve the value after =
        default = default.strip() #remove white space

    elif release4:
        f = open(allCFG, "r")
        for line in f:
            #find the section namcfg
            if 'namcfg' in line: 
                #print(line)
                for line in f:
                    if "cn_domcfg" in line:
                        defaultK = line
        f.close()

        domcfg_fname = defaultK.split('=')[1].lstrip().split(' ')[0].replace('"', '') + '.nc'
        
        try:
            ds = nc.Dataset(domcfg_fname)
            # NC variable 'ORCA_index' in domaincfg = jp_cfg in old namelist_cfg
            iorca = int(ds['ORCA'][:])
            if  iorca == 1:
                default = "ORCA" 
            else:
                default = "UNKNOWN"
        except FileNotFoundError:
            print("could not read from " + domcfg_fname)
        except:
            print("Variable 'ORCA' could not be found in " + domcfg_fname)
 
    print(PURPLE + default.strip() + NORMAL)
    return default.strip()      


def get_vgridtype():
    '''This function will return the value corresponding to the vertical grid type from namelist_cfg file. Returns unknown if value is not available'''
    stringToMatch = '&namzgr '
    default = ""
    #get list of namelists
    allCFG = getNameLists()
    #remove empty spaces
    allCFG = allCFG.replace(" ", "")
    result = ""

    print("\n --> Vertical grid type. Accept with [ENTER]:\n\n")
    
    #MMS:{
    if release3:
        f = open(allCFG, "r")
        
        for line in f:
            if line.startswith(stringToMatch):
                #print("line is ", line) # comma on the end prevents the double spacing from printing a file line
                for line in f:
                    ##namzgrLst.append(line)
                    if (".true." in line):
                        #print("Filtered ", line)
                        #add to list to extract
                        #lnLst.append(line)
                        for ext in line:
                            if("zco" in line):
                                default = "zco (z-coordinate with full steps)"
                                #print(BOLD + "Vertical Grid Type: " + NORMAL + "" + default)
                                break
                            elif("zps" in line):
                                default = "zps (z-coordinate with partial steps)"
                                #print(BOLD + "Vertical Grid Type: " + NORMAL + "" + default)
                                break
                            elif("sco" in line):
                                default = "sco (s- or hybrid z-s-coordinate)"
                                #print(BOLD + "Vertical Grid Type: " + NORMAL + "" + default)
                                break
                            #not clear - refer to bash script
                            elif ("isfcav" in line):
                                default = "ice shelf cavity"
                                #print(BOLD + "Vertical Grid Type: " + NORMAL + "" + default)
                                break
                            
                        
                    if line.startswith("/"):
                        break # stop this inner for loop; outer loop picks up on the next line      
                    
    elif release4:
        f = open(allCFG, "r")
        for line in f:
            #find the section namcfg
            if 'namcfg' in line: 
                #print(line)
                for line in f:
                    if "cn_domcfg" in line:
                        defaultK = line
        f.close()

        domcfg_fname = defaultK.split('=')[1].lstrip().split(' ')[0].replace('"', '') + '.nc'
        
        try:
            ds = nc.Dataset(domcfg_fname)
            # NC variable 'ORCA_index' in domaincfg = jp_cfg in old namelist_cfg
            if ds['ln_zco'][0]:
                default = "zco (z-coordinate with full steps)"
                #print(BOLD + "Vertical Grid Type: " + NORMAL + "" + default)
            elif ds['ln_zps'][0]:
                default = "zps (z-coordinate with partial steps)"
                #print(BOLD + "Vertical Grid Type: " + NORMAL + "" + default)
            elif ds['ln_sco'][0]:
                default = "sco (s- or hybrid z-s-coordinate)"
                #print(BOLD + "Vertical Grid Type: " + NORMAL + "" + default)
            #not clear - refer to bash script
            elif ds['ln_isfcav'][0]:
                default = "ice shelf cavity"
                #print(BOLD + "Vertical Grid Type: " + NORMAL + "" + default)

        except FileNotFoundError:
            print("could not read from " + domcfg_fname)
    #:MMS}
    
    if default =="":
        print(PURPLE + "Unknown" + NORMAL)
        return "Unknown"
    else:
        print(PURPLE + default + NORMAL)    
        return default       
 

def get_hgridpt():
    '''This function will return the value corresponding to the hortizonatal grid type from namelist_cfg file. Returns unknown if value is not available'''
    
    stringToMatch = 'namcfg'
    defaultx = ""
    defaulty = ""
    output = 0
     #get list of namelists
    allCFG = getNameLists()
    #remove empty spaces
    allCFG = allCFG.replace(" ", "")
#
    print("\n --> Number of grid points in the horizontal. Accept with [ENTER]: \n\n")
  
    #MMS:{
    if release3:
        f = open(allCFG, "r")
        #print("\n File name: ", line)
        for line in f:
            #find the section namcfg
            if stringToMatch in line: 
                #print(line)
                for line in f:
                    if "jpidta" in line:
                        defaultx = line
                    #continue printing until line matches "/"
                    if "jpjdta" in line:
                    #if endStringToMatch2 in line:
                        defaulty = line
                        break
                    

        #extract digits only from defaultX
        outputX=0
        repl_str = re.compile('^\d+$')
        line = defaultx.split()
        for word in line:
                match = re.search(repl_str, word)
                if match:
                    outputX = float(match.group())
    
   
        #extract digits only from defaultY
        
        outputY=0
        #repl_str = re.compile('\d+.?\d*')
        repl_str = re.compile('^\d+$')
        #t = r'\d+.?\d*'
        line = defaulty.split()
        for word in line:
                match = re.search(repl_str, word)
                if match:
                    outputY = float(match.group())
                    #multiply two points
                    #output = outputX * outputY
                    output = str(outputX) + " x " + str(outputY)
                    #print(BOLD + "Horizontal Grid Points (I x J):" +NORMAL+ " "+ str(output))

    elif release4:
        f = open(allCFG, "r")
        for line in f:
            #find the section namcfg
            if 'namcfg' in line: 
                #print(line)
                for line in f:
                    if "cn_domcfg" in line:
                        defaultK = line
        f.close()

        domcfg_fname = defaultK.split('=')[1].lstrip().split(' ')[0].replace('"', '') + '.nc'
        
        try:
            ds = nc.Dataset(domcfg_fname)
            # NC variable 'ORCA_index' in domaincfg = jp_cfg in old namelist_cfg
            outputX = int(ds['jpiglo'][0])
            outputY = int(ds['jpjglo'][0])

        except FileNotFoundError:
            print("could not read from " + domcfg_fname)
            
        output = str(outputX) + " x " + str(outputY)
    #:MMS}

                    
    if str(output) =="":
        print(PURPLE + "Unknown" + NORMAL)
        return "Unknown"
    else:
        print(PURPLE + str(output) + NORMAL)    
        return str(output)       
            
def get_vgridpt():
    '''This function will return the number of grid points in  vertical grid from namelist_cfg file. Returns unknown if value is not available'''
    stringToMatch = 'namcfg'
    defaultK = ""
    output = 0
     #get list of namelists
    allCFG = getNameLists()
    #remove empty spaces
    allCFG = allCFG.replace(" ", "")

    print("\n --> Number of grid points in the vertical? Accept with [ENTER]: \n\n")

    #MMS:{
    if release3:
    
        f = open(allCFG, "r")
    
        for line in f:
            #find the section namcfg
            if stringToMatch in line: 
                #print(line)
                for line in f:
                    if "jpkdta" in line:
                        defaultK = line
                        break
                    
        #print(defaultK)

        #extract digits only from defaultK
        
        output=0
        repl_str = re.compile('^\d+$')
        line = defaultK.split()
        for word in line:
                match = re.search(repl_str, word)
                if match:
                    output = float(match.group())
                    #print(BOLD + "Vertical Grid Points (K): " + NORMAL + "" + str(output))
                    
    elif release4:
        f = open(allCFG, "r")
        for line in f:
            #find the section namcfg
            if 'namcfg' in line: 
                #print(line)
                for line in f:
                    if "cn_domcfg" in line:
                        defaultK = line
        f.close()

        domcfg_fname = defaultK.split('=')[1].lstrip().split(' ')[0].replace('"', '') + '.nc'
        
        try:
            ds = nc.Dataset(domcfg_fname)
            # NC variable 'ORCA_index' in domaincfg = jp_cfg in old namelist_cfg
            output = int(ds['jpkglo'][0])

        except FileNotFoundError:
            print("could not read from " + domcfg_fname)
            
    #:MMS}
                    
                    
    if str(output) =="":
        print(PURPLE + "Unknown" + NORMAL)
        return "Unknown"
    else:
        print(PURPLE + str(output) + NORMAL)    
        return str(output)


def get_atmos():
    '''This function will return the number of surface boundary condition from namelist_cfg file. Returns unknown if value is not available'''
    
    stringToMatch = '&namsbc '
    matchedLine = ''
    namsbcLst=[] #stores all elements in &namsbc
    lnLst=[] #stores all ln_ elements
    nnLst=[] #stores all nn_ elements
    vaxLst=[] #stores the prefix e.g. blk_core, ana etc..
    v="" #returns the line with .true.
    vax=""
    default=""
    defaultadd=""

    #get list of namelists
    allCFG = getNameLists()
    #remove empty spaces
    allCFG = allCFG.replace(" ", "")

    print("\n --> Defining the surface boundary condition. Accept with [ENTER]: \n\n")

    f = open(allCFG, "r")
    for line in f:
        if stringToMatch in line:
            matchedLine = line
            for line in f:
                if not (line.startswith("/")):
                         namsbcLst.append(line)
                else:
                    break
    
    #check for ln_ 
    for item in namsbcLst:
        if item.find("ln_") != -1:
            lnLst.append(item)
  
    for i in lnLst:
         if "true" in i:
           v = i
          
           #get last part after the ln_
           _index = v.find("_")
           eqIndex = v.find("=")
           vax = v[_index+1:eqIndex] #retrieve the value after _
           vax = vax.strip() #remove white spaces
           vaxLst.append(vax)
    
    for v in vaxLst:
        if(v == "ana"):
            default = "Analytical forcing"
            #output = BOLD + "Surface Boundary Condition:  " + NORMAL + "" + default
            #print(output)
        elif (v == "flx"):
            default = "Flux formulation"
            #output = BOLD + "Surface Boundary Condition:  " + NORMAL + "" + default
            #print(output)
        elif (v == "blk_clio"):
            default = "CLIO bulk formulation"
            #output = BOLD + "Surface Boundary Condition:  " + NORMAL + "" + default
            #print(output)
        elif (v == "blk_core"):
            default = "CORE bulk formulation"
            #output = BOLD + "Surface Boundary Condition:  " + NORMAL + "" + default
            #print(output)
        elif (v == "blk_mfs"):
            default = "MFS bulk formulation"
            #output = BOLD + "Surface Boundary Condition:  " + NORMAL + "" + default
            #print(output)
        elif (v == "cpl"):
            default = "Coupled to atmosphere"
            #output = BOLD + "Surface Boundary Condition:  " + NORMAL + "" + default
            #print(output)
        elif (v == "mixcpl"):
            default = "Forced & coupled atmosphere"
            #output = BOLD + "Surface Boundary Condition:  " + NORMAL + "" + default
            #print(output)
        elif (v == "blk"):
            default = "Bulk formulae formulation"
        elif (v == "rnf"):
            defaultadd = " + separate runoff"
    
    # check for nn_ 
    for itemN in namsbcLst:
        if itemN.find("nn_fwb") != -1:
             #get the digits between = and .
            eqIndex = itemN.find("=")
            dotIndex = itemN.find("!")
            output = itemN[eqIndex+1:dotIndex] #retrieve the value after _
            output = output.strip() #remove white spaces

    if release4:
        f.seek(0)
        for line in f:
                if '&namsbc_blk' in line:
                    matchedLine = line
                    for line in f:
                        if not (line.startswith("/")):
                                namsbcLst.append(line)
                        else:
                            break
    
        #check for ln_ 
        for item in namsbcLst:
            if item.find("ln_") != -1:
                lnLst.append(item)

        for i in lnLst:
            if "true" in i:
                v = i
                
                #get last part after the ln_
                _index = v.find("_")
                eqIndex = v.find("=")
                vax = v[_index+1:eqIndex] #retrieve the value after _
                vax = vax.strip() #remove white spaces
                vaxLst.append(vax)
        
        for v in vaxLst:
            if(v == "NCAR"):
                default = default + ", NCAR algorithm   (Large and Yeager 2008)"
                #output = BOLD + "Surface Boundary Condition:  " + NORMAL + "" + default
                #print(output)
            elif (v == "COARE_3p0"):
                default = default + ", COARE 3.0 algorithm   (Fairall et al. 2003)"
                #output = BOLD + "Surface Boundary Condition:  " + NORMAL + "" + default
                #print(output)
            elif (v == "COARE_3p5"):
                default = default + ", COARE 3.5 algorithm   (Edson et al. 2013)"
                #output = BOLD + "Surface Boundary Condition:  " + NORMAL + "" + default
                #print(output)
            elif (v == "EXMWF"):
                default = default + ", ECMWF algorithm   (IFS cycle 31)"
                #output = BOLD + "Surface Boundary Condition:  " + NORMAL + "" + default
                #print(output)

    #:MMS}
        
    if default =="":
        print(PURPLE + "Unknown" + NORMAL)
        return "Unknown"
    else:
        print(PURPLE + default + defaultadd + " + Freshwater Budget Correction (Mode " + output + ")" + NORMAL)    
        return str(default + defaultadd + " + Freshwater Budget Correction (Mode " + output + ")")


def get_oceanrdt() :
    '''This function will return the length of the general ocean time step for dynamics from namelist_cfg file. Returns unknown if value is not available'''
    
    stringToMatch = 'namdom'
    defaultT = ""
    output = 0
    allCFG = getNameLists()
    #remove empty spaces
    allCFG = allCFG.replace(" ", "")

    print("\n --> The length of the general ocean time step for dynamics. Accept with [ENTER]: \n\n")

    f = open(allCFG, "r")
    
    for line in f:
        if stringToMatch in line: 
            #print(line)
            for line in f:
                if "rn_rdt" in line:
                    defaultT = line
                    #get the digits between = and .
                    eqIndex = defaultT.find("=")
                    dotIndex = defaultT.find(".")
                    output = defaultT[eqIndex+1:dotIndex] #retrieve the value after _
                    output = output.strip() #remove white spaces
                    #print(BOLD + "Time Step for Dynamics [sec]: " + NORMAL + "" + str(output))
                    break
        
    #get the digits between = and .
    eqIndex = defaultT.find("=")
    dotIndex = defaultT.find(".")
    output = defaultT[eqIndex+1:dotIndex] #retrieve the value after _
    output = output.strip() #remove white spaces

    if str(output) =="":
        print(PURPLE + "Unknown" + NORMAL)
        return "Unknown"
    else:
        print(PURPLE + str(output) + NORMAL)    
        return str(output)


def get_nestnumber():   
    '''This function will ask for user input to enter number of AGRIF Nests. Returns 0 if value is not available'''
    
    default = 0 
    
    print("\n --> How many "+ BOLD + "AGRIF nests "+NORMAL+" are  embedded? Accept our guess with [ENTER] or [M]odify accordingly: \n\n")
    print(PURPLE +  "Nest Number: "+ NORMAL+  "is "+ str(default))
    choice = input()
    choice = choice.lower()
    if choice == 'm':
        default = input("Input value: ")
        return default
    else:
        return default

#
def get_passivetracers(): 
    '''This function will ask for user input which additional passive tracers are implemented. Returns unknown if value is not available'''
    
    default = "Unknown"
    
    print("\n --> Which additional passive tracers are implemented? Accept our guess with [ENTER] or [M]odify accordingly: \n\n")
    print(PURPLE + "List of passive tracers (TOP): "+ NORMAL+  "is "+ default)
    choice = input()
    choice = choice.lower()
    if choice == 'm':
        default = input("Input value: ")
        return default
    else:
        return default

def check_inputDef_exists():
    '''This function checks whether input.def file exists in the directory of the chosen configuration. If not the script will exit.'''
    
    if(CURRCONFIG == True):
       parent = os.path.dirname(os.getcwd()) 
    else:
       parent = os.getcwd() 
    
    #print("Parent ", parent)
    found = False
    files = []
    #r=root, d=directories, f = files
    for r, d, f in os.walk(parent):
        for file in f:
            if 'input.def' in file:
                found = True
                files.append(os.path.join(r, file))

    if found == True:
        return True
    else:
        return False

#MMS:{    
def list_inputfiles():
    '''The purpose of this function is to generate the 'Input Files' section in the readme file '''

    SEPARATOR = '------------------'
    TABLE_HEADER = ["**NEMO Input File**", '**Reference (DOI)**', '**Download**']
    markdown = "| {} |\n".format(" | ".join(TABLE_HEADER))
    markdown += '| '
    for i in TABLE_HEADER:
        markdown += SEPARATOR
        markdown += ' | '

    markdown += '\n'

    config = configparser.ConfigParser()
    config.read('input.ini')
    NemoFileNames = config.sections()
        
    for sec in NemoFileNames:
        url = "[download]({})".format(config[sec]['URL'])
        ref = config[sec]['Reference']
        doi = config[sec]['DOI']
        if doi:
            doi = "([doi:{0}](https://doi.org/{0}))".format(doi)
        refdoi = " ".join([ref,doi])
        markdown += "| {} | {} | {} |\n".format(sec,refdoi,url)

    return markdown + '\n'
#:MMS}

def list_inputfiles_old():
    '''The purpose of this function is to generate the 'Input Files' section in the readme file '''
    
    #count 0 is the header
    count = 1
    col1=""
    col2=""
    col3=""
    col3up=""
    
    path2 = os.getcwd() 
    parent = os.path.dirname(path2) #parent directory
    
    #for (dirname, dirs, files) in os.walk('.'):
    for (dirname, dirs, files) in os.walk(parent):
       rowsLst.append([])
       rowsLst.append([])
       rowsLst.append([]) 
       
       for filename in files:
           if filename.endswith('.def') :
               thefile = os.path.join(dirname,filename) #list path with .def extension
               with open(thefile) as f:
                   url = ""
                   infile_nemo = ""
                   #print all contents of the file
                   for line in f:
                       line = line.strip()
                       
                       #access only the lines that are not commented and empty
                       if not (line.startswith('#')):
                            if len(line)!=0:
                               allFieldsFirstLine = line.split(",")
                               try:
                                    infile_nemo = allFieldsFirstLine[0]#1st element
                                    #print("infile_nemo: "  + infile_nemo)
                                    col1 = infile_nemo
                                    if infile_nemo == "" or infile_nemo == "\\":
                                        infile_nemo = next(f) #move to next line
                                    else:
                                        infile_nemo = allFieldsFirstLine[1]
                               except:
                                    #print("Error for infile_nemo")
                                    print("infile Nemo: "  + infile_nemo)
                               
                               try:
                                    url = allFieldsFirstLine[2]
                                    #tableListing.append(url)
                                    if not(url == "\\" or url == "" or url == "'\'"):
                                        #print("this is the original line")
                                        url = allFieldsFirstLine[2]    
                                    else:
                                        #print("this is the next line")
                                        url = next(f) #move to next line
                                    #print("url: " + url.strip())
                                    col3 = url.strip() + "\n"
                               except:
                                    #two exceptions to cater for in file
                                    #./ORCA025.L46.LIM2vp.CFCSF6.JRA.XIOS2/EXP00/input.def
                                    #print("Skip two lines section")
                                    url = next(f)
                                    url = next(f)
                                    #print("URL : ", url.strip())
                                    col3 = url.strip() + "\n"
                               
                               #add data to table     
                               col1 = col1.strip()
                               col2 = "---"
                               col3 = col3.strip()
                                                             
                               if 'thredds' in col3:
                                   col3up = col3
                                   pass
                               elif '@' in col3:
                                   getIndex = col3.find('@')
                                   col3 = col3[getIndex + 1:]
                                   #replace : with /
                                   col3 = col3.replace(':', '/')
                                   #get last part of the string
                                   lastPart = col3.split("/")[-1]
                                   lastIndex = col3.find(lastPart)
                                   col3 = col3[:lastIndex-1]
                                   col3up = lastPart + "<b>" + " in " + "</b>" + col3
                                   #col3up = lastPart + "<b>" + " in " + "</b>" + "<a href=" + "'" + col3 + "'" + ">" + col3 + "</a>"
                                                                  
                              
                               rowsLst[count].append(col1)
                               rowsLst[count].append(col2)
                               rowsLst[count].append(col3up)
                               
                               count = count + 1
                            
               #### Create the table #######
    
               rowsLst[0].append("**NEMO Input File**")
               rowsLst[0].append("**Reference (DOI)**")
               rowsLst[0].append("**Download**")
               
               #this list will not contain empty tuples and will be used in the markdown template
               rowsLst2 = [e for e in rowsLst if e]
               return make_markdown_table(rowsLst2)
                  
def make_markdown_table(rowsLst2):
    '''This function is used to format the tables in the readme file to replicate the markdown format '''
    
    markdown = "\n" + str("| ")
    
    for e in rowsLst2[0]:
        to_add = " " + str(e) + str(" |")
        markdown += to_add
    markdown += "\n"
    
    markdown += '|'
    for i in range(len(rowsLst2[0])):
        markdown += str("-------------- | ")
    markdown += "\n"
    
    for entry in rowsLst2[1:]:
        markdown += str("| ")
        for e in entry:
            to_add = str(e) + str(" | ")
            markdown += to_add
        markdown += "\n"
    
    return markdown + "\n"   


def config_table():
    '''The purpose of this function is to generate the 'Configuration' section in the readme file '''
    
    configLst = [
                    ["**Characteristic**", "**Specs**"],["**Working repository**", _CURREPO_],
                    ["**Nemo-ocean repository**", _NEMOREPO_],["**Branch**", _NEMOBRANCH_],
                    ["**Nemo-ocean revision**",_NEMOREVISION_ ],["**Components**", _COMPONENTS_],
                    ["**Reference Configuration**", _REFCONFIG_], ["**CPP keys**", _CPPKEYS_],
                    ["**Grid**", _GRID_], ["**Resolution**", _RESOLUTION_],
                    ["**Horizontal Gridpoints**", _HGRIDPT_],["**Vertical Levels**",_VGRIDPTZ_],
                    ["**Atmospheric Condition**", _ATMOS_],["**Time Step [s]**",_OCEANRDT_],
                    ["**Passive Tracers**", _PASSIVTRACERS_],["**Number of Nests**",_NESTNUMBER_ ],
                    
                ] 
    markdown = "\n" + str("| ")
    
    for e in configLst[0]:
        to_add = " " + str(e) + str(" |")
        markdown += to_add
    markdown += "\n"
    
    markdown += '|'
    for i in range(len(configLst[0])):
        markdown += str("-------------- | ")
    markdown += "\n"
    
    for entry in configLst[1:]:
        markdown += str("| ")
        for e in entry:
            to_add = str(e) + str(" | ")
            markdown += to_add
        markdown += "\n"
    
    return markdown + "\n"   

def check_confdir():     
    '''The purpose of this function is to check if the script is in a configuration sub-folder in NEMOGCM/CONFIG '''
    pathLst=[]
    currentDirectory = os.getcwd()
    words = currentDirectory.split("/",4)
    for w in words:
        pathLst.append(w)
        
    lastElement = str(pathLst[len(pathLst) -1]) #should be CONFIG
    print("last Element ", lastElement)
    if(lastElement != "CONFIG"):
        errmsg("It seems, we are not in a configuration sub-folder of NEMOGCM/CONFIG. I'm lost. " + BOLD + "Please run this script within a configuration folder!" + NORMAL)
    
def check_prereq():
    '''This function will check some prerequisits, like git vs svn, curl & wget,... '''
    #MMS:{
    #'''This function will check that EXP00 or EXPREF directory is present in the current file structure '''
    #if(EXPref != "EXP00") and (EXPref != "EXPREF"):
    #    errmsg("No EXP00/EXPREF folder with default settings was found. Please create one and re-run this script.")
    #else:
    cwflag = 0
    #check_confdir()
    git_X = git.__version__
    if len(git_X ) > 0 :
        sucssmsg("GIT found")
    else:
        errmsg("GIT not found")
        
    svn_X = svn.__version__
    if len(svn_X) > 0 :
        sucssmsg("SVN found")
    else:
        errmsg("SVN not found")
    
    ssh_X = os.system('ssh -V')
    if len(str(ssh_X)) > 0 :
        sucssmsg("SSH found")
    else:
        errmsg("SSH not found")
        
    curl_X = pycurl.version
    if len(curl_X ) > 0 :
        sucssmsg("CURL found")
    else:
        errmsg("CURL not found")
        cwflag = cwflag + 1
    
    wget_X = wget.__version__
    if len(wget_X ) > 0 :
        sucssmsg("WGET found")
    else:
        errmsg("WGET not found")
        cwflag = cwflag + 1
    
    if (cwflag > 0):
        errmsg("Neither CURL nor WGET was found. Abort")
        
    m4_X = os.system('m4 --version')
    if len(str(m4_X)) > 0 :
        sucssmsg("m4 found")
    else:
        errmsg("m4 not found")
    
    global zUSERNAME
    global zUSEREMAIL
    if os.path.isdir(".includes"):
        if os.path.isfile(".includes/.simsar.ini"):
            config = configparser.ConfigParser()
            config.read(".includes/.simsar.ini")
            zUSERNAME = parser.get('GLOBAL', 'username')
            zUSEREMAIL = parser.get('GLOBAL', 'useremail')
    else:
        os.mkdir(".includes")
    
    global zGITSERVER
    zGITSERVER = get_zGITSERVER()
    
    global zGITNMSPC
    zGITNMSPC= get_zGITNMSPC()
        
    print("zGITSERVER: ",zGITSERVER)
    print("zGITNMSPC: ",zGITNMSPC)
    #:MMS}
     
def get_zGITSERVER():
        '''This function returns the value of a variable zGITSERVER'''    
        if (LNGIT == True):
            zGITSERVER="git.geomar.de"
        else:
            zGITSERVER="github.com"

        return zGITSERVER

def get_zGITNMSPC():
        '''This function returns the value of a variable zGITNMSPC'''    
        zGITSERVER  = get_zGITSERVER()
            
        if zGITSERVER == "github.com":
            zGITNMSPC="immerse-project"
        
        
        elif zGITSERVER == "git.geomar.de":
            zGITNMSPC="NEMO/EXP"
            
        return zGITNMSPC
    
    
def get_zPAGESRV():
        '''This function returns the value of a variable zPAGESRV'''   
        zGITSERVER  = get_zGITSERVER()
            
        if zGITSERVER == "github.com":
            zPAGESRV="https://immerse.github.io"
            zPAGE=zPAGESRV + "/" + _CONFNAME_
        
        
        elif zGITSERVER == "git.geomar.de":
            zPAGESRV="#"
            zPAGE = "|  [Static Page]("+zPAGESRV+"/"+_CONFNAME_+")"
            
        return zPAGE
    
def prep_note(): 
        '''The purpose of this function is to display a list of prerequistes to successfully render a readme file'''
        uName = os.uname().nodename
        uName = str(uName)
        print("\n")
        hr()
        print("\n")
        center("Prepare NEMO Simulation Upload with SIMSAR")
        print("\n")
        hr()
        print("\n\n Before we begin, we have to make sure, that the following " + ULINE + "conditions are fulfilled" + NORMAL + " and you have the " + ULINE + "essential information" + NORMAL + " at hand right now:")
        print("\n\n")
        indent(" [ ] " "You have access to " + BOLD + BLACK + "at least one git server" + NORMAL + " and your " + BOLD + BLACK + "public ssh-key " + NORMAL + "from this host ("+uName+") has been deposited under your git server profile.") 
        print("\n")
        indent(" [ ] " "Configuration-specific " + BOLD + BLACK + " input files " + NORMAL + " are " + ULINE + "publicly accessible" + NORMAL + " at least for members of a specific group) and you have a " + BOLD + BLACK +" reference" + NORMAL + " (e.g. DOI) and a " + BOLD + BLACK + " Download-URL " + NORMAL + " for each file.")
        print("\n")
        indent(" [ ] " "You know the " + BOLD + BLACK + "NEMO revision"+NORMAL+" and the "+BOLD+ BLACK + "URL"+NORMAL+" you've installed it from (if it can't be determined automatically, because you're not within a svn or git working directory)")
        print("\n")
        indent(" [ ] " "If your configuration is build upon another "+BOLD+BLACK + "reference configuration " + NORMAL +" you'll need the exact name and a reference URL (e.g. another simulation's repository)")
        print("\n")
        indent(" [ ] " "Is the file '"+BOLD+BLACK+"input.ini"+NORMAL+"' part of this configuration? " )
        print("\n")
        
        answer = input(BOLD + GREEN + "Do you confirm, that you meet the conditions above? [y|N]:" + NORMAL)
        answer = answer.lower()
        if(answer == "n"):
            exit()
        else:
            return answer


def template():
    '''The purpose of this function is to create a markup template with values generated from previous functions'''
              
    readme = Template(""" 
                      
# {{_CONFNAME_}}-{{_EXPNAME_}}
___

[Purpose](#purpose)  |  [Contact](#contact)  |  [License](#license)  |  [Configuration](#configuration) | [Input Files](#input-files)  |  [Diagnostics](#diagnostics)  | [Installation](#installation)

____

## Purpose

{{_PURPOSE_}}


## Contact

{{_CONTACT_}}


## Terms of Use

**By downloading this repository and using this code you agree to the following conditions.**

The code in this project is based on the [NEMO](http://www.nemo-ocean.eu) software (Copyright (c) Centre National de la Recherche Scientifique CNRS).

The original code as well as the contribution to this code in this project are licensed under the conditions of [CeCILL](http://www.cecill.info). 

The person stated under '*Contact*' above is the owner of the intellectual property rights of these contributions and **must be informed afore** publishing and **must be cited** in every published work that is based completely or partially on the modifications and additional code provided by this configuration.

Usage is at one's own risk. 


## Configuration
{{config_table}}

## Experiment/Simulation

<!--//DELDEL
The default settings for this experiment can be found in the [{{_EXPNAME_}}]({{_EXPNAME_}}) folder.
The modified code is located in the [MY_SRC](MY_SRC) directory.
DELDEL//-->
       
### Input Files

*  **NEMO Input File:** File names as they are expected by NEMO  
*  **Reference:** Citation for an article or report, webpage or even better: DOI  
*  **Download:** Link for direct downloading the file (no user-interaction preferred to make it script-compliant)  


{{list_inputfiles}}

## Diagnostics

See [DIAG](DIAG) for some standard diagnostics from a simulation with this configuraton.

## Installation

There are plenty of ways how to install a local copy of this configuration:

1. You can [clone it with git](#install-with-git) (regardless of whether your NEMOGCM path is already under git control or not). 
2. Or you just download an archive from the web interface.  

In some cases there are different versions of the same configuration in separate branches (e.g. to reflect different NEMO revisions); **check the branches/tags** menu on the web interface or use the git branch and checkout commands to select 
the version you're interested in.


## Install with git


#### (A) NEMOGCM not under git control

If your NEMO installation **is not under git control already**, you can clone this configuration using the URL specified on the project's front page:

Go into the **configurations directory** in your local NEMO installation (`CONFIG/` for NEMO version 3, `cfgs/` for version 4) and clone this project (see the "Clone" link or button on the git webinterface to get the URL).

**EXAMPLE:** In this example, NEMO (version 4) has been installed on a separate scratch-disk (`$WORK`) and the simulation repository was hosted on github under the namespace `$GITNAMESPACE`:

~~~bash
cd $WORK/NEMO-release-4.0/cfgs
git clone git@github:${GITNAMESPACE}}/{{_CONFNAME_}}-{{_EXPNAME_}}.git
cat {{_CONFNAME_}}-{{_EXPNAME_}}/{{_EXPNAME_}}/exp_cfg.txt >> ./work_cfgs.txt
~~~

You can also specify a certain branch when cloning (e.g. `release-4.0` if it exists):

~~~bash
git clone -b release-4.0 git@github:${GITNAMESPACE}}/{{_CONFNAME_}}-{{_EXPNAME_}}.git
~~~

This wil create a new configuration folder, which can be used as a reference case for **`makenemo -r`**. 
Make sure, you add this configuration  to the local registry file `cfg.txt` (NEMO version 3) or `work_cfgs.txt` (NEMO version 4) before invoking **`makenemo`**.



#### (B) NEMOGCM already under git control

If your **NEMOGCM installation is already under git control** you cannot clone a different repository into the existing working copy. 
Instead, you can use **`git subtree`** to inject files from another remote repository into a particular sub-folder of your existing working tree.

Within NEMOGCM directory:

**Option - With git commands**

~~~bash
cd $WORK/NEMO-release-4.0
git remote add -f remote_{{_CONFNAME_}}-{{_EXPNAME_}} git@{{_zGITSERVER_}}:{{_zGITNMSPC_}}/{{_CONFNAME_}}-{{_EXPNAME_}}.git   # add remote
git subtree add --prefix CONFIG/{{_CONFNAME_}}-{{_EXPNAME_}} remote_{{_CONFNAME_}}-{{_EXPNAME_}} {{_NEMOBRANCH_}} --squash     # donwload master branch into sub-folder
cat cfgs/{{_CONFNAME_}}-{{_EXPNAME_}}/{{_EXPNAME_}}/exp_cfg.txt >> cfgs/work_cfgs.txt
~~~

> In this case, you keep the information from where you have downloaded the reference configuration (see \`git remote -v\`).

Or even shorter, without keeping remote source information (not recommended):

~~~bash
cd $WORK/NEMO-release-4.0
git subtree add --prefix cfgs/{{_CONFNAME_}}-{{_EXPNAME_}} git@{{_zGITSERVER_}}:{{_zGITNMSPC_}}/{{_CONFNAME_}}-{{_EXPNAME_}}.git {{_NEMOBRANCH_}} --squash
cat cfgs/{{_CONFNAME_}}-{{_EXPNAME_}}/{{_EXPNAME_}}/exp_cfg.txt >> cfgs/work_cfgs.txt
~~~


#### Other revisions

The revision that will be installed, is the most recent one from the **master** branch. 
If you're seeking another branch/revision of this configuration (e.g. an older one), you can browse available branches/tags via the web-interface or list alternative 
branches on the command line and swap available branches/tags easily with \`checkout\`:

~~~bash
cd {{_CONFNAME_}}-{{_EXPNAME_}}
git branches -r
git checkout otherBranch
~~~

Note: *origin/HEAD* in the output listing is not a branch in its own but points to the default branch (master branch in most cases).
        
        """)

    fillenv()
    
    pathS = pathlib.Path().absolute()

    #MMS:{
    RUN="-"+run
    #if (LNGIT==True) and (CURRCONFIG==False):
        #READMEOUT = str(pathS) + "/CONFIG/" + exp + "/README_"+exp+RUN+".md"
       
    #elif (LNSVN==True) and (CURRCONFIG==False) and (release3 == True):
        #READMEOUT = str(pathS) + "/NEMOGCM/CONFIG/" + exp +  "/README_"+exp+RUN+".md"
        
    #elif (LNSVN==True) and (CURRCONFIG==False) and (release4 == True):
        #READMEOUT = str(pathS) + "/cfgs/" + exp  +  "/README_"+exp+RUN+".md"
        
    ##if current script is stored in one of the configurations
    #elif (CURRCONFIG == True):
        #READMEOUT = str(pathS) + "/README_"+exp+RUN+".md"
    ##MMS-------------------------
    #READMEOUT = str(pathS) + "/README_"+exp+RUN+".md"
    READMEOUT = str(pathS) + "/README.md"
    #:MMS}
    
    with open(READMEOUT, "w") as f:
        f.write(readme.render(
                _CONFNAME_ = _CONFNAME_,
                _EXPNAME_ = _EXPNAME_,
                _CONTACT_ = _CONTACT_, 
                _PURPOSE_=_PURPOSE_,                     
                _CURREPO_=_CURREPO_,
                _NEMOREPO_= _NEMOREPO_,
                _NEMOREVISION_=_NEMOREVISION_,
                _NEMOBRANCH_ =_NEMOBRANCH_,
                _COMPONENTS_ =_COMPONENTS_,
                _REFCONFIG_=_REFCONFIG_,
                _CPPKEYS_ = _CPPKEYS_,
                _RESOLUTION_=_RESOLUTION_,
                _GRID_ = _GRID_,
                _HGRIDPT_=_HGRIDPT_,
                _VGRIDPTZ_=_VGRIDPTZ_,
                _ATMOS_ = _ATMOS_,
                _OCEANRDT_ = _OCEANRDT_,
                _NESTNUMBER_= _NESTNUMBER_,
                _PASSIVTRACERS_ = _PASSIVTRACERS_,
                list_inputfiles = list_inputfiles(),
                config_table = config_table(),
                _zGITSERVER_ = _zGITSERVER_,
                _zGITNMSPC_ = _zGITNMSPC_,
                _zPAGE_ = _zPAGE_
                ))
    print("README file created")

################ main program ########################

scriptLoc=""
scriptLoc = checkScriptLocation()
#print("script loc ", scriptLoc)
if scriptLoc != None:
    exp = scriptLoc
else:
    exp=""
#MMS run : variable holding the experiment's name.
run=""

getNemoConfig()

#{MMS:
#EXPref = check_EXPref()
#if (EXPref == True) and (release3 == True):
    #EXPref = "EXP00"
#elif (EXPref == True) and (release4 == True):
    #EXPref = "EXPREF"
#else:
    #EXPref = "EXP00 is not in this directory"

#:MMS}

#
color()
#
hr()
center("Technical Details")
hr()
#
check_gitorsvn()
#
get_zGITNMSPC()
#
#    #
check_prereq()
#
ans = prep_note()
#
#call the main function

if(ans == 'y') and (exp == ""):
#    print("Exp 1 ", exp)
    main() #if script is stored in the root

elif(ans == 'y') and (exp != ""):
#    print("Exp 2 ", exp)
    mainconfig() #if script is stored in a particular configuration
    

