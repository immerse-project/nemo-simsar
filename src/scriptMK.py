#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 08 13:07:20 2020

@author: luciennemicallef, markusscheinert

"""

import git
import os
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

class color:
        '''This class stores a list of colours and font styles'''
        RED ='\033[31m'
        GREEN ='\033[32m'
        YELLOW ='\033[93m'
        BLUE ='\033[34m'
        PURPLE ='\033[35m'
        BLACK ='\033[30m'
        NORMAL ='\033[0m'
        ULINE ='\033[04m'
        BOLD ='\033[1m'



#instance for class color
c = color()

class ReadmeScript:
    '''This method is used for initialising and accessing the following attributes from other methods'''        
    def __init__(self):
        
        self.LNGIT=False
        self.LNSVN=False
        self.CURRCONFIG=False
        self.zPAGE=""
        self.zPAGESRV=""        
        self.zGITSERVER=""
        self.zGITNMSPC=""
        self.release3=False
        self.release4=False
        self.exp = ""
        self.run = ""
        self.inputIniPath=""

    def getNemoConfig(self):
        '''This function will look for the directory 'NEMOGCM/CONFIG' for release 3 and 'cfgs' for release 4
        anywhere in the system'''
        #global release3, release4
        #MMS:{
        configPath="test"
        rootPath = os.getcwd()
        
        if "/CONFIG/" in rootPath:
            self.release3=True
            configPath = ''.join(rootPath.partition("CONFIG")[:2])
        elif "/cfgs/" in rootPath:
            self.release4=True
            configPath = ''.join(rootPath.partition("cfgs")[:2])
        elif "/REF" in rootPath:
            self.release4=True
            #if the configuration is not stored in cfgs
            #configPath = ''.join(rootPath.partition("trunk")[:1])
            configPath = rootPath
        else:
            configPath = rootPath
        return configPath
        #:MMS}
        

    def mainconfig(self):
         '''This function will be called if the script is initially saved in one of the configuration folders'''
         self.check_inputIni_exists()
         #check if input.def is part of this directory
         if self.check_inputIni_exists() == True:
            if self.ask_exp00(self.exp) == True:
                self.template()
            else:
                print("Exiting..Please start again")
         else:
            print("Input.ini file does not exist, create this file to be able to proceed")
            
        
    def getAllConfigFolders(self):
        '''This function will return a list of configurations, and eventually user will choose 
            which configuration s/he would like to work with:
            (e.g. AMM12, ORCA2_LIM_CFC_C14b, GYRE, ORCA025.L46.LIM2vp.CORE.XIOS1, ORCA2_LIM etc..
            Display only the configurations that include EXP00 folder'''
    
        configFolders=[]
        listWithAllDir = []
        listOnlyExp00=[]
    
        configPath = self.getNemoConfig()
        #print("Config path" , configPath)
        
        for r, d, f in os.walk(configPath):
            for directory in d:
                if "EXP00" in d: #release3
                    listWithAllDir.append(os.path.join(r,directory))
                elif "EXPREF" in d: #release 4
                    listWithAllDir.append(os.path.join(r,directory))
                elif "REF" in d: #release 4
                    listWithAllDir.append(os.path.join(r,directory))
                
        for i in listWithAllDir:
           if "EXP00" in i:
               #remove the EXP00 
               listOnlyExp00.append(i)
           elif "EXPREF" in i:
               #remove the EXPREF 
               listOnlyExp00.append(i)
           elif "REF" in i:
               #remove the EXPREF 
               listOnlyExp00.append(i)
               
           
        for c in listOnlyExp00:
            last = c.split('/')
            configFolders.append(last[-2])
       
        #sort configFolders
        configFolders.sort()
        return configFolders
    
                
    def checkScriptLocation(self):
        '''The purpose of this function is to check whether the script is being run from a particular configuration'''
        path2 = os.getcwd()
        configName = os.path.basename(path2)
        
        if configName == "REF": 
            currPath = os.path.abspath(os.curdir)
            os.chdir("..")
            configPath = os.path.abspath(os.curdir)
            configName = os.path.basename(configPath)
            
        if configName == "trunk": 
            currPath = os.path.abspath(os.curdir)
            os.chdir("..")
            configPath = os.path.abspath(os.curdir)
            configName = os.path.basename(configPath)
        
        for x in self.getAllConfigFolders():
                if x == configName:
                    CURRCONFIG = True
                    return x
                else:
                    CURRCONFIG = True
                    return configName
        
    def fillenv(self):          
        '''This function returns variables which will be used to create the readme file'''
        _CONFNAME_= self.get_confname()                    
        _EXPNAME_= self.get_expname()
        _CONTACT_= self.get_username() + " - " + self.get_useremail() 
        _PURPOSE_= get_purpose()
        _CURREPO_= self.get_currepo()
        _NEMOREPO_=self.get_nemorepo()
        _NEMOREVISION_= self.get_nemorevision()
        _NEMOBRANCH_= self.get_branch()
        _COMPONENTS_ = self.get_components()
        _REFCONFIG_= self.get_refconfig()
        _CPPKEYS_= self.get_cppkeys() 
        _RESOLUTION_= self.get_resolution()
        _GRID_ = self.get_hgridtype() + ", " + self.get_vgridtype()
        _HGRIDPT_= self.get_hgridpt()
        _VGRIDPTZ_=self.get_vgridpt()
        _ATMOS_=self.get_atmos()
        _OCEANRDT_ =  self.get_oceanrdt()
        _NESTNUMBER_= get_nestnumber()
        _PASSIVTRACERS_ = get_passivetracers()
        _zGITSERVER_ = self.get_zGITSERVER()
        _zGITNMSPC_ = self.get_zGITNMSPC()
        _zPAGE_ = self.get_zPAGESRV(_CONFNAME_)
        
        return _CONFNAME_, _EXPNAME_, _CONTACT_, _PURPOSE_, _CURREPO_,_NEMOREPO_, _NEMOREVISION_, _NEMOBRANCH_, _COMPONENTS_, _REFCONFIG_, _CPPKEYS_, _RESOLUTION_, _GRID_, _HGRIDPT_, _VGRIDPTZ_, _ATMOS_,_OCEANRDT_,_NESTNUMBER_, _PASSIVTRACERS_, _zGITSERVER_, _zGITNMSPC_, _zPAGE_
        
     
    def ask_exp00(self, exp):
       '''exp is the configuration name'''
       '''The purpose of this function is to show all directories for the chosen configuration '''
       
       print("\nChosen configuration is : ",exp)
            
       #list to store all the directories inside this configuration
       listWithAllDir = []
       configPath = self.getNemoConfig()
       #configPath = self.getNemoConfig() + "/"+exp             
       for directories in glob.glob("*/**/", recursive=True):
           listWithAllDir.append(directories)
            
       #sort list
       listWithAllDir.sort()
       print("\nDirectories for the above configuration: ")
       for i in listWithAllDir:
           print(i)
     
       choice = input("\n --> Are you sure that this is the configuration you would like to work with? Proceed with [Y] or [N] \n\n")
       choice = choice.lower()
       if choice == 'y':
           return True
       else:
           return False
          
       
    def check_gitorsvn(self):
        '''The purpose of this function is to check whether the current script is stored as a git repo or as an svn repo'''
        '''if LNGIT is True - the script is stored as a git repo'''
        '''if LNSVN is True - the script is stored as an svn svn repo'''
       
        try:
            #MMS repo = git.Repo(".", search_parent_directories=True)
            repo = git.Repo("../../", search_parent_directories=True)
        except git.InvalidGitRepositoryError:
            print(c.BLUE + "This is not a git repo \n" + c.NORMAL)
            
        else:
            print(c.BLUE + "This is a Git Repo" + c.NORMAL)
            self.LNGIT=True
        
        if (self.LNGIT == False):
             try:
                subprocess.check_output("svn info", stderr=subprocess.STDOUT, shell=True)
             except subprocess.CalledProcessError as e:
                if e.output.decode("utf-8").startswith('svn: '):
                    print(c.BLUE + "This is not an svn repo \n" + c.NORMAL)
                else:
                    print("Error - ", e)
             except OSError as e: 
                print("Error - ", e)
             else:
                print(c.BLUE + "This is an SVN Repo" + c.NORMAL)
                #global LNSVN
                self.LNSVN=True     
        
    def get_confname(self):
        '''Returns the configuration name which is the variable stored as 'exp'  '''
        print("\n --> What is the name you want to use for publishing this configuration ? Our first guess is, that it's the configuration name in the current path. Accept with [ENTER] or modify accordingly:\n\n")  
        currentDirectory = os.getcwd()
    
        print(c.PURPLE+"Configuration's name: "+self.exp+""+ c.NORMAL)#returns the chosen configuration by the use
        return self.exp
        
    def get_expname(self):
        '''Returns the name of the current experiment folder'''
        currentDirectory = os.getcwd()
        self.run = os.path.basename(currentDirectory)
        
        print(c.PURPLE+"Experiment's name: "+self.run+""+c.NORMAL)
        return self.run
    
    def get_username(self):
        '''This function returns the username, if available in the config file '''
            
        if(self.LNGIT == True):
            try:
                repo = git.Repo(".", search_parent_directories=True)
                print("\n --> What is your full name? We try to get it from git. Accept with [ENTER] or modify accordingly: \n\n")
                reader = repo.config_reader()
                default = reader.get_value('user','name')
                output = c.PURPLE + "User's Full Name :" + c.default + c.NORMAL
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
        
        if(self.LNSVN == True):
            try:
                username = input("\n --> What is your name? Enter your full name (temporarily) \n\n")    
                return username
            except KeyboardInterrupt:
                print("Exit..")
        
    
    def get_useremail(self):      
         '''This function returns the user email, if available in the config file '''
         if(self.LNGIT == True):
             try:
                 repo = git.Repo(".", search_parent_directories=True)
                 print("\n --> What is your email address? We try to get it from git. Accept with [ENTER] or modify accordingly: \n\n")
                 reader = repo.config_reader()
                 default = reader.get_value('user','email')
                 output = c.PURPLE + "User's email :" + default + c.NORMAL
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
        
         if(self.LNSVN == True):
            try: 
                email = input("\n --> Enter your email address (temporarily) or press [Ctrl-C] to exit and update through git-init \n\n")    
                return email
            except KeyboardInterrupt:
                print("Exit.. ")
    
    def get_currepo(self):
        '''The purpose of this function is to display the actual repo from were NEMO was cloned'''
        print("\n --> Are we in a git/svn working tree? And from which remote repository was NEMOGCM cloned? Try to get it from git/svn. Accept with [ENTER]:\n")
        
        default=""
        revision=""
        
        if(self.LNGIT==True):
            try:
                repo = git.Repo(".", search_parent_directories=True)
                remoteLocation = repo.remote("origin").url
                default = remoteLocation
                
                if(default != "") & (self.LNGIT == True):
                    print(c.PURPLE + "This is a GIT Repo " + c.NORMAL)
                    print(c.PURPLE + "Actual Repository = "  + default + "" + c.NORMAL)
                    return default
            
            except git.InvalidGitRepositoryError:
                print(c.PURPLE + "Not connected to GIT" + c.NORMAL)
        else: 
            pass
                    
        if(self.LNSVN == True):
            try:
                #MMS default = subprocess.check_output("svn info | awk '/^URL:/ {print $2}'", shell=True).strip()
                default = subprocess.check_output("LC_ALL=C svn info --show-item url", shell=True).strip()
                revision = subprocess.check_output("LC_ALL=C svn info --show-item revision", shell=True).strip().decode().replace("'", "")
                #convert to string
                default = str(default)
                default = default.replace("'", "")
                if revision == "":
                    print(c.RED + "SVN repository found, but current directory has not been committed" + c.NORMAL)
                elif(default != "") & (self.LNSVN == True) & (revision != ""):
                    print(c.PURPLE + "This is an SVN Repo " + c.NORMAL)
                    print(c.PURPLE + "Actual Repository = " + str(default[1:]) +  c.NORMAL)
                    return default[1:]
                else:
                    print(c.RED + "Not connected to SVN" + c.NORMAL)
                    
            except subprocess.CalledProcessError as e:
                    if e.output.decode("utf-8").startswith('svn: '):
                        print(c.BLUE + "This is not an svn repo \n" + c.NORMAL)
                    else:
                        print("Error - ", e)
            except OSError as e: 
                        print("Error - ", e)
            
            #except svn.exception.SvnException:
            #    print("This is not a working copy of SVN - Not connected to SVN")'''
            
        else:
            pass
    
    def get_nemorepo(self):
        '''This function displays the URL of the repository the NEMO was installed from '''
        print("\n\n\n --> What is the URL of the repository you installed NEMO from? Try to get it from git/svn. Accept with [ENTER]:")    
        if(self.LNGIT==True):
            getIndexHash=""
            #command = '--grep="jussieu" --pretty=oneline --abbrev-commit --reverse | cut -d ' ' -f 3 |head -n 1'
            proc = subprocess.check_output(["git", "log", "--pretty=oneline", "--abbrev-commit", "--reverse"])
            proc = str(proc)
            getSvnIDText = proc.find('http')
            getIndexHash = proc.find('@')
            getUrl = proc[getSvnIDText:getIndexHash]
            print(c.PURPLE + ""+ getUrl + "" + c.NORMAL)
            return(getUrl)
        
        if(self.LNSVN==True):
            #command = '--grep="jussieu" --pretty=oneline --abbrev-commit --reverse | cut -d ' ' -f 3 |head -n 1'
            #MMS getURLsvn = subprocess.check_output("svn info | awk '/^URL:/ {print $2}'", shell=True).strip()
            getURLsvn = subprocess.check_output("LC_ALL=C svn info --show-item url $(LC_ALL=C svn info --show-item wc-root)", shell=True).strip()
            getURLsvn = str(getURLsvn)
            getURLsvn = getURLsvn.replace("'", "")
            print(c.PURPLE + ""+ str(getURLsvn[1:]) + "" + c.NORMAL)
            return(getURLsvn[1:])
    
       
    def get_nemorevision(self):
        '''This function will display the revision number for the current NEMO version '''
        print("\n\n\n --> What is the NEMO revision you're currently using? Try to get it from git/svn history. Accept with [ENTER]:")
        if(self.LNGIT == True):
            try:
                proc = subprocess.check_output(["git", "log", "--pretty=oneline", "--abbrev-commit", "--reverse"])
                proc = str(proc)
                getSvnIDText = proc.find('http')
                getIndexHash = proc.find('#')
                nemoRev1 = proc[getSvnIDText:getIndexHash]
                getAT = nemoRev1.find('@')
                getspace = nemoRev1.find(' ')
                nemoRev2 = nemoRev1[getAT+1:getspace]
                print(c.PURPLE + nemoRev2 + c.NORMAL)
                return(nemoRev2)
            except git.InvalidGitRepositoryError:
                print(c.PURPLE + "Not connected to GIT" + c.NORMAL)
            except OSError as e:
                print("Error - ", e)
        
        if(self.LNSVN==True):
            try:
                #MMS nemoRev = subprocess.check_output("svn info | awk '/^Revision:/ {print $2}'", shell=True).strip()
                nemoRev = subprocess.check_output("LC_ALL=C svn info --show-item revision $(LC_ALL=C svn info --show-item wc-root)", shell=True).strip()
                nemoRev = str(nemoRev)
                nemoRev = nemoRev.replace("'", "")
                print(c.PURPLE + str(nemoRev[1:]) + c.NORMAL)
                return(nemoRev[1:])
            except subprocess.CalledProcessError as e:
                    if e.output.decode("utf-8").startswith('svn: '):
                        print(c.BLUE + "This is not an svn repo \n" + c.NORMAL)
                    else:
                        print("Error - ", e)
            except OSError as e: 
                        print("Error - ", e)
             
    def get_branch(self):
        '''This function will return the branch number for this repo'''
        print("\n")
        print("--> Which branch are you using? Try to get it from git/svn. Accept with [ENTER]: ")
        if (self.LNGIT==True):
            repo = git.Repo(".", search_parent_directories=True)
            default = repo.active_branch
            print(c.PURPLE + str(default)+c.NORMAL)
            return default
        #else:
            #print ("LNGIT is false")
        
        if (self.LNSVN==True):
            #MMS getBranchInfo = subprocess.check_output("svn info | awk '/^URL:/ {print $2}'", shell=True).strip()
            getBranchInfo = subprocess.check_output("LC_ALL=C svn info --show-item url $(LC_ALL=C svn info --show-item wc-root)", shell=True).strip()
            getBranch = str(getBranchInfo)
            branchSplit = getBranch.split('/')
            #MMS branchSplit = getBranch.split('NEMO')
            #Get the last part of the string
            getBranch = branchSplit[-1]
            #MMS getBranch = branchSplit[1]
            getBranch  = getBranch.replace("'","")
            print(c.PURPLE + str(getBranch)+ c.NORMAL)
            return getBranch
        #else:
            #print ("LNSVN is false")
            
    
    
    def get_components(self):
        '''This function returns the NEMO components for this repo from cfg.txt or ref_cfg.txt'''
        output=""
        cfgPath=""
        cfgPath2=""
        componentsLst=[]
        findExactComponent=[]
        path=""
        componentsLst.append('\n')
        print("\n --> What NEMO components are we using? Try to get a comma-separated list from cfg.txt (or ref_cfgs.txt or work_cfgs.txt). Accept with [ENTER]: \n")
        #get file path for /cfg.txt
        currentDirectory = self.getNemoConfig()
        
        #MMS:{
        if self.release3 == True:
            path = os.path.join(currentDirectory, "cfg.txt")
            cfgPath = open(path, "r")
            #cfgPath = open("../../cfg.txt", "r")
        elif self.release4 == True:
            if self.exp == 'ORCA2_ICE':
                for path in glob.iglob(currentDirectory + '/**/work_cfgs.txt', recursive = True): 
                    cfgPath2 = open(path, "r")   
                    
            else:
                for path in glob.iglob(currentDirectory + '/**/ref_cfgs.txt', recursive = True): 
                    cfgPath2 = open(path, "r")
        else:
            for path in glob.iglob(currentDirectory + '/**/work_cfgs.txt', recursive = True): 
                    cfgPath2 = open(path, "r")   
                                
        #used for scenario where configuration is cloned to the local machine
    
        #:MMS}
        for i in cfgPath:
            if self.exp in i:
                componentsLst.append(i.strip())
        #MMS:{
        if cfgPath2:
            for i in cfgPath2:
                if self.exp in i:
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
                if item.split(' ')[0] == self.exp:
                    #Get the first element from the last
                    #output = str(pathSplit[0])
                    output = ', '.join(item.split(' ')[1:])
                #:MMS}
        #MMS:{
        comp = ''.join([str(elem) for elem in output])
        f = open("../exp_cfg.txt", "w")
        f.write("{}  {}".format(self.exp,comp.replace(',','')))
        f.close()
        
        print(c.PURPLE + comp + c.NORMAL)
        return comp
        #:MMS}
    
    
    def get_refconfig(self):
        '''This function asks for user input to return the reference configuration for a particular configuration. This may also be left blank '''
        zrefconfname=""
        zrefconfurl=""
        zrefconfname = input("--> Name: If there is a reference configuration this particular configuration is based on, please type the name. Otherwise leave it blank by typing [ENTER].\n")
        zrefconfurl = input("--> URL: If there is a reference configuration this particular configuration is based on, please type the URL. Otherwise leave it blank by typing [ENTER].\n")
        return zrefconfname + " - " + zrefconfurl
    
    
    def get_cppkeys(self):
         '''This function searches for .fcm file and extracts the cpp keys'''
         matchPath = ""
         p = os.getcwd()
    
    # #MMS:{    
         
         for x in glob.iglob(p+'/**/cpp_'+self.exp+'.fcm', recursive=True):
            matchPath = x
        
          #matchPath = glob.glob('*cpp_'+exp+'.fcm')
        
         try:
              x = open(matchPath, "r")
              #x = open(''.join(matchPath), "r")
              cppkeysContents = x.read()
              x.close()
         except:
              print('Could not open'+'../cpp_'+self.exp+'.fcm')
              raise
    #:MMS}
                
          #remove bld::tool::fppkeys by replacing this text empty text
          #sample: bld::tool::fppkeys key_diaeiv key_dynldf_c2d
         content = cppkeysContents.replace('\n', ' ')
         content = content.replace('bld::tool::fppkeys ', '')
         return ''.join(str(content))
     
        
        #matchPath = ""
      
    #MMS:{    
         
    #     path = os.path.abspath(os.curdir)
    #     try:
    #         for root, dirs, files in os.walk(path):
    #             for file in files:
    #                 if file.endswith('.fcm'):
    #                     print("file is ", file)
    #                     x = open(file, "r")
    #                     cppkeysContents = x.read()
    #                     x.close()
    #     except FileNotFoundError:
    #          print('Could not open: '+'cpp_'+self.exp+'.fcm')
    #          raise
    # #:MMS}
                
    #      #remove bld::tool::fppkeys by replacing this text empty text
    #      #sample: bld::tool::fppkeys key_diaeiv key_dynldf_c2d
    #     content = cppkeysContents.replace('\n', ' ')
    #     content = content.replace('bld::tool::fppkeys ', '')
    #     return ''.join(str(content))
             
    def getNameLists(self):
        ''' This function searches for namelist_cfg file and extracts the namelist path for the chosen configuration'''    
        #to retrieve only the cfg of the chosen configuration
        cfgNameLists = []
        findExactNameList = []
        output = ""
        
        #MMS:{        
        path2 = self.getNemoConfig()
        for (dirname, dirs, files) in os.walk(path2):
        #for (dirname, dirs, files) in os.walk('.'):
            for filename in files:
                if filename.startswith('1_namelist_cfg'):
                    pass #ignore
                elif 'namelist_cfg' in filename :
                    thefile = os.path.join(dirname,filename)
                    if self.exp in thefile:
                        cfgNameLists.append(thefile)
                        
        #go through the list to check for entries containing part of the chosen name
        if(len(cfgNameLists) == 1):
            #print(cfgNameLists)
            output = cfgNameLists
             
        else:
            #add each item to the list
            for i in range(len(cfgNameLists)):
                findExactNameList.append(cfgNameLists[i])
            #Search through each item for the exact configuration name
            for item in findExactNameList:
                #for i in item:
                    pathSplit = item.split('/')
                    #Get the third element from the last
                    if self.exp == pathSplit[-3]:
                        #print(item)
                        output = item #return full path
            
        #convert list to str
        return ''.join([str(elem) for elem in output])
        
        ##MMS-----------
        
        #return './namelist_cfg'
    
        #:MMS}
            
    def get_resolution(self):
        '''This function will return the value corresponding to the resolution 
        of the horizontal grid from namelist_cfg file. Returns unknown if value is not available '''
        
        stringToMatch = 'namcfg'
        defaultK = ""
        output = 0
         #get list of namelists
        allCFG = self.getNameLists()
        print("+++get_resolution: allCFG=", end='')
        print(allCFG)
        #remove empty spaces
        allCFG = allCFG.replace(" ", "")
    
        print("\n --> The resolution of the horizontal grid. Accept with [ENTER]: \n\n")
        
        #MMS:{
        if self.release3:
        
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
    
        elif self.release4:
            f = open(allCFG, "r")
            for line in f:
                #find the section namcfg
                if stringToMatch in line: 
                    for line in f:
                        if "cn_domcfg" in line:
                            defaultK = line
                         
            f.close()
            print("default K is ", defaultK)
            if (defaultK != ""):
                #print("default K is ", defaultK)
                domcfg_fname = defaultK.split('=')[1].lstrip().split(' ')[0].replace('"', '') + '.nc'
                print("domcfg_fname is ", domcfg_fname)
                try:
                    ds = nc.Dataset(domcfg_fname, "r")
                    print("ds is ", domcfg_fname)
                    # NC variable 'ORCA_index' in domaincfg = jp_cfg in old namelist_cfg
                    output = ds['ORCA_index'][:]
                    print("output is ", output)
                except FileNotFoundError:
                    print("could not read from " + domcfg_fname)
                except:
                    print("ORCA_Index not found in " + domcfg_fname)
                            
            else:
                print("Could not find cn_domcfg")
            
        #print(defaultK)
        #extract digits only from defaultK
        print(c.PURPLE + str(output) + c.NORMAL)
        return str(output)
        
    def get_hgridtype(self):
        '''This function will return the value corresponding to the horizontal grid type from namelist_cfg file. Returns unknown if value is not available'''
        stringToMatch = 'namcfg'
        matchedLine = ''
        endStringToMatch2 = "cp_cfg"
        output = ""
        #get list of namelists
        allCFG = self.getNameLists()
        #remove empty spaces
        allCFG = allCFG.replace(" ", "")
        result = ""
        default = ""
        defaultK = ""
        
    
        print("\n --> Horizontal grid type, e.g. ORCA for a global tri-polar grid. Accept our guess with [ENTER]:\n\n")
        
        f = open(allCFG, "r")
        #MMS:{
        if self.release3:
    
            #go through the list of files with namelist_cfg
            for line in f:
                if stringToMatch in line:
                    #print("Matched Line ", matchedLine)             
                    for line in f:
                        result = result + line
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
    
        elif self.release4:
            #f = open(allCFG, "r")
            for line in f:
                #find the section namcfg
                if 'namcfg' in line: 
                    #print(line)
                    for line in f:
                        if "cn_domcfg" in line:
                            defaultK = line
           
            if (defaultK != ""):
                domcfg_fname = defaultK.split('=')[1].lstrip().split(' ')[0].replace('"', '') + '.nc'
                print("domcfg_fname  ", domcfg_fname)
                try:
                    ds = nc.Dataset(domcfg_fname, "r")
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
            
            else:
                print("Could not find cn_domcfg")
        
        f.close()
 
        print(c.PURPLE + default.strip() + c.NORMAL)
        return default.strip()      
    
    
    def get_vgridtype(self):
        '''This function will return the value corresponding to the vertical grid type from namelist_cfg file. Returns unknown if value is not available'''
        stringToMatch = '&namzgr '
        default = ""
        defaultK = ""
        #get list of namelists
        allCFG = self.getNameLists()
        #remove empty spaces
        allCFG = allCFG.replace(" ", "")
    
        print("\n --> Vertical grid type. Accept with [ENTER]:\n\n")
        
        #MMS:{
        if self.release3:
            f = open(allCFG, "r")
            
            for line in f:
                if line.startswith(stringToMatch):
                    for line in f:
                        ##namzgrLst.append(line)
                        if (".true." in line):
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
                        
        elif self.release4:
            f = open(allCFG, "r")
            for line in f:
                #find the section namcfg
                if 'namcfg' in line: 
                    #print(line)
                    for line in f:
                        if "cn_domcfg" in line:
                            defaultK = line
            f.close()
    
            if (defaultK != ""):
                domcfg_fname = defaultK.split('=')[1].lstrip().split(' ')[0].replace('"', '') + '.nc'
                
                try:
                    ds = nc.Dataset(domcfg_fname, "r")
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
                    
                except:
                    print("Could not be found in " + domcfg_fname)
            
            else:
                print("Could not find cn_domcfg")
        #:MMS}
        
        if default =="":
            print(c.PURPLE + "Unknown" + c.NORMAL)
            return "Unknown"
        else:
            print(c.PURPLE + default + c.NORMAL)    
            return default       
     
    
    def get_hgridpt(self):
        '''This function will return the value corresponding to the hortizonatal grid type from namelist_cfg file. Returns unknown if value is not available'''
        
        stringToMatch = 'namcfg'
        defaultx = ""
        defaulty = ""
        defaultK = ""
        output = 0
         #get list of namelists
        allCFG = self.getNameLists()
        #remove empty spaces
        allCFG = allCFG.replace(" ", "")
    #
        print("\n --> Number of grid points in the horizontal. Accept with [ENTER]: \n\n")
      
        #MMS:{
        if self.release3:
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
    
        elif self.release4:
            outputX=0
            outputY=0
            f = open(allCFG, "r")
            for line in f:
                #find the section namcfg
                if 'namcfg' in line: 
                    #print(line)
                    for line in f:
                        if "cn_domcfg" in line:
                            defaultK = line
            f.close()
    
            if (defaultK != ""):
                domcfg_fname = defaultK.split('=')[1].lstrip().split(' ')[0].replace('"', '') + '.nc'
                
                try:
                    ds = nc.Dataset(domcfg_fname, "r")
                    # NC variable 'ORCA_index' in domaincfg = jp_cfg in old namelist_cfg
                    outputX = int(ds['jpiglo'][0])
                    outputY = int(ds['jpjglo'][0])
        
                except FileNotFoundError:
                    print("could not read from " + domcfg_fname)
                
                except:
                    print("jpiglo and jpjglo could not be found in " + domcfg_fname)
            
                    
                output = str(outputX) + " x " + str(outputY)
        #:MMS}
            else:
                print("Could not find cn_domcfg")
    
                        
        if str(output) =="":
            print(c.PURPLE + "Unknown" + c.NORMAL)
            return "Unknown"
        else:
            print(c.PURPLE + str(output) + c.NORMAL)    
            return str(output)       
                
    def get_vgridpt(self):
        '''This function will return the number of grid points in  vertical grid from namelist_cfg file. Returns unknown if value is not available'''
        stringToMatch = 'namcfg'
        defaultK = ""
        output = 0
        defaultK = ""
         #get list of namelists
        allCFG = self.getNameLists()
        #remove empty spaces
        allCFG = allCFG.replace(" ", "")
    
        print("\n --> Number of grid points in the vertical? Accept with [ENTER]: \n\n")
    
        #MMS:{
        if self.release3:
        
            f = open(allCFG, "r")
        
            for line in f:
                #find the section namcfg
                if stringToMatch in line: 
                    #print(line)
                    for line in f:
                        if "jpkdta" in line:
                            defaultK = line
                            break
                        
            #extract digits only from defaultK
            
            output=0
            repl_str = re.compile('^\d+$')
            line = defaultK.split()
            for word in line:
                    match = re.search(repl_str, word)
                    if match:
                        output = float(match.group())
                        #print(BOLD + "Vertical Grid Points (K): " + NORMAL + "" + str(output))
                        
        elif self.release4:
            f = open(allCFG, "r")
            for line in f:
                #find the section namcfg
                if 'namcfg' in line: 
                    #print(line)
                    for line in f:
                        if "cn_domcfg" in line:
                            defaultK = line
            f.close()
    
            if(defaultK != ""):
                domcfg_fname = defaultK.split('=')[1].lstrip().split(' ')[0].replace('"', '') + '.nc'
                
                try:
                    ds = nc.Dataset(domcfg_fname, "r")
                    # NC variable 'ORCA_index' in domaincfg = jp_cfg in old namelist_cfg
                    output = int(ds['jpkglo'][0])
        
                except FileNotFoundError:
                    print("could not read from " + domcfg_fname)
                
                except:
                    print("jpkglo could not be found in " + domcfg_fname)
                
        #:MMS}
            else:
                print("Could not find cn_domcfg")
                
    
        if str(output) =="":
            print(c.PURPLE + "Unknown" + c.NORMAL)
            return "Unknown"
        else:
            print(c.PURPLE + str(output) + c.NORMAL)    
            return str(output)
    
    
    def get_atmos(self):
        '''This function will return the number of surface boundary condition from namelist_cfg file. Returns unknown if value is not available'''
        
        stringToMatch = '&namsbc '
        matchedLine = ''
        namsbcLst=[] #stores all elements in &namsbc
        lnLst=[] #stores all ln_ elements
        vaxLst=[] #stores the prefix e.g. blk_core, ana etc..
        v="" #returns the line with .true.
        vax=""
        default=""
        defaultadd=""
        output=""
    
        #get list of namelists
        allCFG = self.getNameLists()
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
    
        if self.release4:
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
                elif (v == "COARE_3p0"):
                    default = default + ", COARE 3.0 algorithm   (Fairall et al. 2003)"
                elif (v == "COARE_3p5"):
                    default = default + ", COARE 3.5 algorithm   (Edson et al. 2013)"
                elif (v == "EXMWF"):
                    default = default + ", ECMWF algorithm   (IFS cycle 31)"
    
        #:MMS}
            
        if default =="":
            print(c.PURPLE + "Unknown" + c.NORMAL)
            return "Unknown"
        else:
            print(c.PURPLE + default + defaultadd + " + Freshwater Budget Correction (Mode " + output + ")" + c.NORMAL)    
            return str(default + defaultadd + " + Freshwater Budget Correction (Mode " + output + ")")
    
    
    def get_oceanrdt(self) :
        '''This function will return the length of the general ocean time step for dynamics from namelist_cfg file. Returns unknown if value is not available'''
        
        stringToMatch = 'namdom'
        defaultT = ""
        output = 0
        allCFG = self.getNameLists()
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
                        break
            
        #get the digits between = and .
        eqIndex = defaultT.find("=")
        dotIndex = defaultT.find(".")
        output = defaultT[eqIndex+1:dotIndex] #retrieve the value after _
        output = output.strip() #remove white spaces
    
        if str(output) =="":
            print(c.PURPLE + "Unknown" + c.NORMAL)
            return "Unknown"
        else:
            print(c.PURPLE + str(output) + c.NORMAL)    
            return str(output)
    
    
    
    
    def check_inputIni_exists(self):
        '''This function checks whether input.ini file exists in the directory of the chosen configuration. If not the script will exit.'''
          
        if(self.CURRCONFIG == True):
           parent = os.getcwd()
        else:
           parent = os.getcwd() 
        
        found = False
        files = []
        #r=root, d=directories, f = files
        for r, d, f in os.walk(parent):
            for file in f:
                if 'input.ini' in file:
                    found = True
                    files.append(os.path.join(r, file))
                    self.inputIniPath = os.path.join(r, file)
    
        if found == True:
            return True
        else:
            return False
    
    
    
    def check_confdir(self):     
        '''The purpose of this function is to check if the script is in a configuration sub-folder in NEMOGCM/CONFIG '''
        pathLst=[]
        currentDirectory = os.getcwd()
        words = currentDirectory.split("/",4)
        for w in words:
            pathLst.append(w)
            
        lastElement = str(pathLst[len(pathLst) -1]) #should be CONFIG
        print("last Element ", lastElement)
        if(lastElement != "CONFIG"):
            errmsg("It seems, we are not in a configuration sub-folder of NEMOGCM/CONFIG. I'm lost. " + c.BOLD + "Please run this script within a configuration folder!" + c.NORMAL)
        
    def check_prereq(self):
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
            
        '''
        svn_X = svn.__version__
        if len(svn_X) > 0 :
            sucssmsg("SVN found")
        else:
            errmsg("SVN not found")
        '''
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
        
        if os.path.isdir(".includes"):
            if os.path.isfile(".includes/.simsar.ini"):
                config = configparser.ConfigParser()
                config.read(".includes/.simsar.ini")
                zUSERNAME = self.parser.get('GLOBAL', 'username')
                zUSEREMAIL = self.parser.get('GLOBAL', 'useremail')
        else:
            os.mkdir(".includes")
        
        
        self.zGITSERVER = self.get_zGITSERVER()
    
        self.zGITNMSPC= self.get_zGITNMSPC()
            
        print("zGITSERVER: ",self.zGITSERVER)
        print("zGITNMSPC: ",self.zGITNMSPC)
        #:MMS}
         
    def get_zGITSERVER(self):
            '''This function returns the value of a variable zGITSERVER'''    
            if (self.LNGIT == True):
                self.zGITSERVER="git.geomar.de"
            else:
                self.zGITSERVER="github.com"
    
            return self.zGITSERVER
    
    def get_zGITNMSPC(self):
            '''This function returns the value of a variable zGITNMSPC'''    
            self.zGITSERVER  = self.get_zGITSERVER()
                
            if self.zGITSERVER == "github.com":
                self.zGITNMSPC="immerse-project"
            
            
            elif self.zGITSERVER == "git.geomar.de":
                self.zGITNMSPC="NEMO/EXP"
                
            return self.zGITNMSPC
        
        
    def get_zPAGESRV(self, _CONFNAME_):
            '''This function returns the value of a variable zPAGESRV'''   
            self.zGITSERVER  = self.get_zGITSERVER()
                
            if self.zGITSERVER == "github.com":
                self.zPAGESRV="https://immerse.github.io"
                self.zPAGE=self.zPAGESRV + "/" + _CONFNAME_
            
            
            elif self.zGITSERVER == "git.geomar.de":
                self.zPAGESRV="#"
                self.zPAGE = "|  [Static Page]("+self.zPAGESRV+"/"+_CONFNAME_+")"
                
            return self.zPAGE
        #MMS:{    
    def list_inputfiles(self):
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
        #config.read('input.ini')
        config.read(self.inputIniPath)
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

        
    def config_table(self, _CURREPO_,_NEMOREPO_, _NEMOREVISION_, _NEMOBRANCH_, _COMPONENTS_, _REFCONFIG_, _CPPKEYS_, _RESOLUTION_, _GRID_, _HGRIDPT_, _VGRIDPTZ_, _ATMOS_,_OCEANRDT_,_NESTNUMBER_, _PASSIVTRACERS_):
        '''The purpose of this function is to generate the 'Configuration' section in the readme file '''
        
        configLst = [
                        ["**Characteristic**", "**Specs**"],["**Working repository**", _CURREPO_],
                        ["**Nemo-ocean repository**", _NEMOREPO_],["**Branch**", _NEMOBRANCH_],
                        ["**Nemo-ocean revision**", _NEMOREVISION_ ],["**Components**", _COMPONENTS_],
                        ["**Reference Configuration**", _REFCONFIG_], ["**CPP keys**", _CPPKEYS_],
                        ["**Grid**", _GRID_], ["**Resolution**", _RESOLUTION_],
                        ["**Horizontal Gridpoints**", _HGRIDPT_],["**Vertical Levels**", _VGRIDPTZ_],
                        ["**Atmospheric Condition**", _ATMOS_],["**Time Step [s]**", _OCEANRDT_],
                        ["**Passive Tracers**", _PASSIVTRACERS_],["**Number of Nests**", _NESTNUMBER_ ],
                        
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

    def template(self):
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

This will create a new configuration folder, which can be used as a reference case for **`makenemo -r`**. 
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

        _CONFNAME_, _EXPNAME_, _CONTACT_, _PURPOSE_, _CURREPO_,_NEMOREPO_, _NEMOREVISION_, _NEMOBRANCH_, _COMPONENTS_, _REFCONFIG_, _CPPKEYS_, _RESOLUTION_, _GRID_, _HGRIDPT_, _VGRIDPTZ_, _ATMOS_,_OCEANRDT_,_NESTNUMBER_, _PASSIVTRACERS_, _zGITSERVER_, _zGITNMSPC_, _zPAGE_ = self.fillenv()
        
        pathS = pathlib.Path().absolute()
    
        #MMS:{
        RUN="-"+self.run
        ##MMS-------------------------
        READMEOUT = str(pathS) + "/README.md"
        #:MMS}
        
        with open(READMEOUT, "w") as f:
            f.write(readme.render(
                    _CONFNAME_ = _CONFNAME_,
                    _EXPNAME_ = _EXPNAME_,
                    _CONTACT_ = _CONTACT_, 
                    _PURPOSE_= _PURPOSE_,                     
                    _CURREPO_= _CURREPO_,
                    _NEMOREPO_= _NEMOREPO_,
                    _NEMOREVISION_= _NEMOREVISION_,
                    _NEMOBRANCH_ = _NEMOBRANCH_,
                    _COMPONENTS_ = _COMPONENTS_,
                    _REFCONFIG_= _REFCONFIG_,
                    _CPPKEYS_ = _CPPKEYS_,
                    _RESOLUTION_= _RESOLUTION_,
                    _GRID_ = _GRID_,
                    _HGRIDPT_= _HGRIDPT_,
                    _VGRIDPTZ_= _VGRIDPTZ_,
                    _ATMOS_ = _ATMOS_,
                    _OCEANRDT_ = _OCEANRDT_,
                    _NESTNUMBER_= _NESTNUMBER_,
                    _PASSIVTRACERS_ = _PASSIVTRACERS_,
                    list_inputfiles = self.list_inputfiles(),
                    config_table = self.config_table(_CURREPO_,_NEMOREPO_, _NEMOREVISION_, _NEMOBRANCH_, _COMPONENTS_, _REFCONFIG_, _CPPKEYS_, _RESOLUTION_, _GRID_, _HGRIDPT_, _VGRIDPTZ_, _ATMOS_,_OCEANRDT_,_NESTNUMBER_, _PASSIVTRACERS_),
                    _zGITSERVER_ = _zGITSERVER_,
                    _zGITNMSPC_ = _zGITNMSPC_,
                    _zPAGE_ = _zPAGE_
                    ))
        print("README file created")
##-- end of class ReadmeScript ---#

def center(text):            
    '''Centers the text to the midddle of the screen'''
    command = ['tput', 'cols']
    width = int(subprocess.check_output(command))
    c = text.center(width)
    print (c)
    print("\n")
    
def errmsg(msg):           
    ''' Displays an error message in RED and reset text colour - Message will be passed as a parameter'''
    print(c.RED + '\n ERROR: ' + msg + '\n\n' + c.NORMAL)
    
def warnmsg(msg):
    ''' Displays an error message in YELLOW and reset text colour - Message will be passed as a parameter'''           
    print(c.YELLOW + '\n WARNING: ' + msg + '\n\n' + c.NORMAL)
    
def sucssmsg(msg):        
    ''' Displays an error message in GREEN and reset text colour - Message will be passed as a parameter'''
    print(c.GREEN + '\n SUCCESS: ' + msg + '\n\n' + c.NORMAL) 
    
def indent(text):
    '''Indents text to the right'''            
    text = textwrap.indent(text, ' ' * 4)[4 - 1:]
    print(text)
        
    
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
        print("\n\n Before we begin, we have to make sure, that the following " + c.ULINE + "conditions are fulfilled" + c.NORMAL + " and you have the " + c.ULINE + "essential information" + c.NORMAL + " at hand right now:")
        print("\n\n")
        indent(" [ ] " "You have access to " + c.BOLD + c.BLACK + "at least one git server" + c.NORMAL + " and your " + c.BOLD + c.BLACK + "public ssh-key " + c.NORMAL + "from this host ("+uName+") has been deposited under your git server profile.") 
        print("\n")
        indent(" [ ] " "Configuration-specific " + c.BOLD + c.BLACK + " input files " + c.NORMAL + " are " + c.ULINE + "publicly accessible" + c.NORMAL + " at least for members of a specific group) and you have a " + c.BOLD + c.BLACK +" reference" + c.NORMAL + " (e.g. DOI) and a " + c.BOLD + c.BLACK + " Download-URL " + c.NORMAL + " for each file.")
        print("\n")
        indent(" [ ] " "You know the " + c.BOLD + c.BLACK + "NEMO revision"+c.NORMAL+" and the "+ c.BOLD+ c.BLACK + "URL"+c.NORMAL+" you've installed it from (if it can't be determined automatically, because you're not within a svn or git working directory)")
        print("\n")
        indent(" [ ] " "If your configuration is build upon another "+c.BOLD+c.BLACK + "reference configuration " + c.NORMAL +" you'll need the exact name and a reference URL (e.g. another simulation's repository)")
        print("\n")
        indent(" [ ] " "Is the file '"+c.BOLD+c.BLACK+"input.ini"+c.NORMAL+"' part of this configuration? " )
        print("\n")
        
        answer = input(c.BOLD + c.GREEN + "Do you confirm, that you meet the conditions above? [Y|N]:" + c.NORMAL)
        answer = answer.lower()
        if(answer == "n"):
            exit()
        else:
            return answer
        
def get_purpose():
        '''This function creates a text file to store the purpose of the readme file or reads the existing text file '''
        #MMS:{
        #pathS = pathlib.Path().absolute()
        pathS = os.getcwd()
        
        dirName = str(pathS) + "/.includes/.recall_purpose.txt"

        if not os.path.exists(dirName):
            with open(dirName, 'w'):
        # Create target Directory
                purpose = input("\n\n --> What's the purpose of this configuration?:\n")
                f = open(dirName, "w")
                f.write(purpose)
                f = open(dirName, "r")
                purpose = f.read()
                print(c.PURPLE + purpose + c.NORMAL)
                return(purpose)
        elif os.path.exists(dirName):
            #with open(dirName, 'w'):
            f = open(dirName, "r")
            #ask if content is as expected
            print("\n\n --> What's the purpose of this configuration? Trying to remember last answer")
            purpose = f.read()
            print(c.PURPLE + purpose + c.NORMAL)
            
            choice = input("Accept with [ENTER] or modify accordingly (press [M] to modify): ")
            choice = choice.lower()
            if choice == 'm':
                purpose = input("Enter a new purpose, this will be overwritten: ")
                f = open(dirName, "w")
                f.write(purpose)
                f = open(dirName, "r")
                purpose = f.read()
                print(c.PURPLE + purpose + c.NORMAL)
                return(purpose)
            else:
                return(purpose)
        
            f.close()
            
        else:
            print("Unable to create this file, check admin rights")


def get_nestnumber():   
        '''This function will ask for user input to enter number of AGRIF Nests. Returns 0 if value is not available'''
        
        default = 0 
        
        print("\n --> How many "+ c.BOLD + "AGRIF nests "+c.NORMAL+" are  embedded? Accept our guess with [ENTER] or [M]odify accordingly: \n\n")
        print(c.PURPLE +  "Nest Number: "+ c.NORMAL+  "is "+ str(default))
        choice = input()
        choice = choice.lower()
        if choice == 'm':
            default = input("Input value: ")
            return default
        else:
            return default
    
def get_passivetracers(): 
        '''This function will ask for user input which additional passive tracers are implemented. Returns unknown if value is not available'''
        
        default = "Unknown"
        
        print("\n --> Which additional passive tracers are implemented? Accept our guess with [ENTER] or [M]odify accordingly: \n\n")
        print(c.PURPLE + "List of passive tracers (TOP): "+ c.NORMAL+  "is "+ default)
        choice = input()
        choice = choice.lower()
        if choice == 'm':
            default = input("Input value: ")
            return default
        else:
            return default