#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 17:30:48 2021

@author: lucienne
"""

import tkinter
import tkinter as tk  # gives tk namespace
from tkinter import *
from tkinter import scrolledtext 
from tkinter.filedialog import asksaveasfilename 
import tkinter.messagebox
import configparser
import string


def addConfig():
    """
    Linked to Add button
    User enters section details. Checks if section name exists and whether the section name includes .nc as an extension
    
    Returns
    -------
    Section name is added to the input.ini and listbox is updated

    """
    try:
        config = configparser.ConfigParser() 
        sectionName = outConfigTxt.get()
        #if section name is empty
        if len(sectionName) == 0:
            tkinter.messagebox.showinfo("Error", "Section name cannot be empty")

        else:
            findExt = sectionName.find('.nc')
            print("value is ", findExt)
            if (findExt==-1):
                sectionName = ''.join((sectionName,'.nc'))
            
            print('SectionName is : ', sectionName)
            #Check if section name exists
            if not config.has_section(sectionName): 
                #Check if section name includes .nc at the end of the string, else add .nc
                config.add_section(sectionName) 
                config.set(sectionName, "URL ", outURLTxt.get()) 
                config.set(sectionName, "Reference ", outReferenceTxt.get()) 
                config.set(sectionName, "DOI ", outDOITxt.get() ) 
                config.set(sectionName, "Checksum ", outCheckSumTxt.get()) 
                config.set(sectionName, "Checksum Type ", outCheckSumTypeTxt.get()) 
                config.set(sectionName, "Comment ", outCommentTxt.get())
        
         
            with open("input.ini", 'a') as configfile: 
                config.write(configfile)
            
            #refresh listbox
            Lb.delete(0, END)
            f = open("input.ini","r")
            for x in f:
                Lb.insert(END,x)
            f.close()
            
            tkinter.messagebox.showinfo("Add", "Section - " + sectionName + " - added")
    
    except:
        tkinter.messagebox.showerror("Error", "Section - " + sectionName + " - cannot be added")

    
def deleteConfig():
    """
    Linked to Delete button
    User enters section name to be deleted 

    Returns
    -------
    If section name is found, it is deleted from the ini file and listbox updated

    """
    
    try:
        config = configparser.ConfigParser()
        config.read("input.ini")
        config.remove_section(outDelTxt.get())
        
        with open("input.ini", 'w') as configfile: 
             config.write(configfile)
        
        #refresh listbox
        Lb.delete(0, END)
        f = open("input.ini","r")
        for x in f:
            Lb.insert(END,x)
            #print(x)
        f.close()
        
        tkinter.messagebox.showinfo("Delete", "Section - " + outDelTxt.get() + " - deleted")
    except:
        tkinter.messagebox.showerror("Error", "Section - " + sectionName + " - cannot be deleted. Check section name.")


def secConfig():
    """
    Linked to Display Button
    
    Returns
    -------

    Display particular section accordingly
    """    
    config = configparser.ConfigParser()
    config.read("input.ini")
    #if config.has_section(outConfigTxt.get()):
    sectionName = outEditTxt.get()
    dictSections = {k:v for k, v in config[sectionName].items()}
      
    outEditSecTxt.delete(1.0,END)    
    
    txtPrint = '\n'.join('{} = {}'.format(k, d) for k, d in dictSections.items())
    outEditSecTxt.insert(END, str(txtPrint)+"\n")
    outEditSecTxt.yview(END)


    
def editConfig():
    """
    Linked to Edit button
    
    User enters section name to be modified 


    Returns
    -------
    An updated list of any modifications in the listbox box and the ini file

    """
    config = configparser.ConfigParser()
    config.read("input.ini")
    sectionName = outEditTxt.get()
    text = outEditSecTxt.get('1.0', END).splitlines()

    #remove section
    if config.has_section(outEditTxt.get()): 
        config.remove_section(outEditTxt.get()) 
    
    #add section
    if not config.has_section(outEditTxt.get()): 
        config.add_section(outEditTxt.get()) 

    for line in text:
     
        #split line to extract the key and value
        splitline = line.split('=')
        key = splitline[0]
        value = splitline[-1]
        config.set(sectionName, key, value)
           
    #config.add_section(outEditSecTxt.get())    
    with open("input.ini", 'w') as configfile: 
        config.write(configfile)
    configfile.close()
     
    #refresh listbox
    Lb.delete(0, END)
    
    f = open("input.ini","r")
    for x in f:
        Lb.insert(END,x)
        #print(x)
    f.close()
    
    tkinter.messagebox.showinfo("Edit", "Section - " + outEditTxt.get() + " - updated")
    
def save(): 
    """
    Download the current ini file as a new file
    
    Returns
    -------
    A new ini file is downloaded and saved containing ALL the sections.
    
    """
    filepath = asksaveasfilename(defaultextension="ini", filetypes=[("INI Files", "*.ini"), ("TXT Files", "*.txt"), ("All Files", "*.*")])
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        output_file.write(''.join(Lb.get(0, END)))
        output_file.write('\n')
        output_file.close()
        
def downloadSection():
    """
    Download just the section requested in the entry

    Returns
    -------
    
    A new ini file is downloaded and saved containing ONLY a particular section, chosen by the user.
    
    """
    
    config = configparser.ConfigParser()
    config.read("input.ini")
    #if config.has_section(outConfigTxt.get()):
    sectionName = outDownTxt.get()
    dictSections = {k:v for k, v in config[sectionName].items()}
       
    txtPrint = '\n'.join('{} = {}'.format(k, d) for k, d in dictSections.items())
    
    #choose filename and location to store the section name
    filepath = asksaveasfilename(defaultextension="ini", filetypes=[("INI Files", "*.ini"), ("TXT Files", "*.txt"), ("All Files", "*.*")])

  
    with open(filepath, 'w') as configfile:
        configfile.write('['+sectionName+']')
        configfile.write('\n')
        configfile.write(''.join(txtPrint))
        configfile.write('\n')
    configfile.close()
     
    tkinter.messagebox.showinfo("Download", "Section - " + outDownTxt.get() + " - downloaded")

def clearAdd():
    """
    Linked to the clear button in the ADD section

    Returns
    -------
    Clear the textboxes

    """
    outConfigTxt.delete(0, END)
    outURLTxt.delete(0, END)
    outReferenceTxt.delete(0, END)
    outDOITxt.delete(0, END)
    outCheckSumTxt.delete(0, END)
    outCheckSumTypeTxt.delete(0, END)
    outCommentTxt.delete(0, END)    

def clearDelete():
    """
    Linked to the clear button in the DELETE section

    Returns
    -------
    Clear the textboxes

    """
    outDelTxt.delete(0, END)
 
def clearEdit():
    
    """
    Linked to the clear button in the EDIT section

    Returns
    -------
    Clear the textboxes

    """
    outEditTxt.delete(0, END)
    outEditSecTxt.delete(0.0, END)
          

""" --- Main program ----"""
form = tk.Tk()

notesConfig = tk.LabelFrame(form, text="")
notesConfig.grid(row=0, columnspan=3, sticky='NW', \
             padx=5, pady=5, ipadx=5, ipady=5)

displayConfig = tk.LabelFrame(form, text=" input.ini: ")
displayConfig.grid(row=1, columnspan=3, sticky='NW', \
             padx=5, pady=5, ipadx=5, ipady=5)
    
downloadConfig = tk.LabelFrame(form, text=" Download ")
downloadConfig.grid(row=2, columnspan=3, sticky='N', \
             padx=5, pady=5, ipadx=5, ipady=5)

genLf = tk.LabelFrame(form, text="")
genLf.grid(row=1, column=9, columnspan=4, \
            sticky='N', padx=5, pady=5, ipadx=5, ipady=5)
    
addLf = tk.LabelFrame(form, text=" Add a new section ")
addLf.grid(row=0, column=9, columnspan=4, \
            sticky='N', padx=5, pady=5, ipadx=5, ipady=5)

delLf = tk.LabelFrame(genLf, text=" Delete a section ")
delLf.grid(row=2, column=9, columnspan=4, sticky='NW', \
              padx=5, pady=5, ipadx=5, ipady=5)

editLF = tk.LabelFrame(genLf, text=" Edit a section: ")
editLF.grid(row=1, column=9, columnspan=4, sticky='NW', \
                padx=5, pady=5, ipadx=5, ipady=5)

#display ini details in label
textvar = StringVar()

textvar ="""NEMO-simsar input file registry
Each NEMO input file has one entry:  
The SECTION name in square brackets is the file name NEMO expects (hard coded or by namelist parameter)
Each section has several key=value pairs:
[NemoFileName.nc]
\tURL = https://
\tReference = Author, A. (YEAR)
\tDOI = <doi:reference-id, not the url>
\tCheckSum = <HASH:sha1|sha224|sha256|sha384|sha512|md5>
\tCheckSumType = [SHA|MD5|]
\tComment = Some additional notes or comments on the data set
"""

outDetailsLbl = tk.Label(notesConfig, text=textvar, wraplength=3000, justify="left")
outDetailsLbl.grid(row=0, column=0, sticky='NW', padx=0, pady=0)

#display the ini details in a listbox   
Lb = Listbox(displayConfig, width=78, height=20)
Lb.config(relief=SUNKEN, border=0)
Lb.grid(row=1, column=0, sticky='E', padx=5, pady=5)
yscroll = Scrollbar(command=Lb.yview, orient=VERTICAL)
yscroll.grid(row=1, column=6, sticky=N + S)
Lb.configure(yscrollcommand=yscroll.set)
    
f = open("input.ini","r")
for x in f:
    Lb.insert(END,x)
    #print(x)
f.close()

outConfigLbl = tk.Label(addLf, text="Enter configuration name:")
outConfigLbl.grid(row=0, column=0, sticky='E', padx=2, pady=2)

outConfigTxt = tk.Entry(addLf)
outConfigTxt.grid(row=0, column=1, columnspan=7, sticky="WE", pady=2)

outURLLbl = tk.Label(addLf, text="Enter URL:")
outURLLbl.grid(row=1, column=0, sticky='E', padx=2, pady=2)

outURLTxt = tk.Entry(addLf)
outURLTxt.grid(row=1, column=1, columnspan=7, sticky="WE", pady=2)

outReferenceLbl = tk.Label(addLf, text="Enter Reference:")
outReferenceLbl.grid(row=2, column=0, sticky='E', padx=2, pady=2)

outReferenceTxt = tk.Entry(addLf)
outReferenceTxt.grid(row=2, column=1, columnspan=7, sticky="WE", pady=2)

outDOILbl = tk.Label(addLf, text="Enter DOI:")
outDOILbl.grid(row=3, column=0, sticky='E', padx=2, pady=2)

outDOITxt = tk.Entry(addLf)
outDOITxt.grid(row=3, column=1, columnspan=7, sticky="WE", pady=2)

outCheckSumLbl = tk.Label(addLf, text="Enter Checksum:")
outCheckSumLbl.grid(row=4, column=0, sticky='E', padx=2, pady=2)

outCheckSumTxt = tk.Entry(addLf)
outCheckSumTxt.grid(row=4, column=1, columnspan=7, sticky="WE", pady=2)

outCheckSumTypeLbl = tk.Label(addLf, text="Enter CheckSum Type:")
outCheckSumTypeLbl.grid(row=5, column=0, sticky='E', padx=2, pady=2)

outCheckSumTypeTxt = tk.Entry(addLf)
outCheckSumTypeTxt.grid(row=5, column=1, columnspan=7, sticky="WE", pady=2)

outCommentLbl = tk.Label(addLf, text="Enter Comment:")
outCommentLbl.grid(row=6, column=0, sticky='E', padx=2, pady=2)

outCommentTxt = tk.Entry(addLf)
outCommentTxt.grid(row=6, column=1, columnspan=7, sticky="WE", pady=2)

outAddBtn = tk.Button(addLf, text="Add", command=addConfig)
outAddBtn.grid(row=6, column=8, sticky='W', padx=5, pady=2)

outClearABtn = tk.Button(addLf, text="Clear", command=clearAdd)
outClearABtn.grid(row=6, column=9, sticky='W', padx=5, pady=2)

outDelLbl = tk.Label(delLf, text="Enter the name of the configuration to remove:")
outDelLbl.grid(row=3, column=0, sticky='W', padx=5, pady=2)

outDelTxt = tk.Entry(delLf)
outDelTxt.grid(row=4, column=0, columnspan=3, pady=2, sticky='WE')

outDelBtn = tk.Button(delLf, text="Delete", command=deleteConfig)
outDelBtn.grid(row=4, column=3, sticky='W', padx=5, pady=2)

outClearCBtn = tk.Button(delLf, text="Clear", command=clearDelete)
outClearCBtn.grid(row=4, column=4, sticky='W', padx=5, pady=2)

outDownAllBtn = tk.Button(downloadConfig, text="Click here to download input.ini", command=save)
outDownAllBtn.grid(row=5, column=0, sticky='W', padx=5, pady=2)

outDownLbl = tk.Label(downloadConfig, text="Enter the name of the section to download:")
outDownLbl.grid(row=6, column=0, sticky='W', padx=5, pady=2)

outDownTxt = tk.Entry(downloadConfig)
outDownTxt.grid(row=6, column=1, columnspan=5, pady=2, sticky='WE')

outDownBtn = tk.Button(downloadConfig, text="Download Section", command=downloadSection)
outDownBtn.grid(row=6, column=6, sticky='W', padx=5, pady=2)

outEditLbl = tk.Label(editLF, \
      text="Enter the name of the section to edit and press Display:")
outEditLbl.grid(row=3, column=0, sticky='W', padx=5, pady=2)

outEditTxt = tk.Entry(editLF, width = 10)
outEditTxt.grid(row=4, column=0, columnspan=3, pady=2, sticky='WE')

outDispBtn = tk.Button(editLF, text="Display...", command=secConfig)
outDispBtn.grid(row=4, column=3, sticky='W', padx=5, pady=2)

outEditSecLbl = tk.Label(editLF, \
      text="Edit the section accordingly and press Edit:")
outEditSecLbl.grid(row=5, column=0, sticky='W', padx=5, pady=2)

outEditSecTxt = scrolledtext.ScrolledText(editLF,  
                                      wrap = tk.WORD,  
                                      width = 70,  
                                      height = 10)  
                                      
outEditSecTxt.grid(row=6, column=0, columnspan=3, pady=2, sticky='WE')

outEditBtn = tk.Button(editLF, text="Edit", command=editConfig)
outEditBtn.grid(row=6, column=3, sticky='W', padx=5, pady=2)

outClearBBtn = tk.Button(editLF, text="Clear", command=clearEdit)
outClearBBtn.grid(row=7, column=3, sticky='W', padx=5, pady=2)


 
tk.mainloop()
