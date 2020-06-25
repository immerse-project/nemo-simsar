# IMMERSE SIMshare

## MKReadme Script for NEMO

## About / Synopsis

* This mkreadme script has been developed to generate a readme file for NEMO configurations on version 3 and version 4.
* Project status: working/prototype

### Features

### Content

Description, sub-modules organization...

### Requirements

1.	A copy of the repository must be saved in the home directory
2.	mkReadme.py must be installed in root of the repository folder or in a particular configuration folder

    Examples:
    home/username/NEMOGCM/mkreadme.py
    or
    home/username/NEMOGCM/AMM12/mkreadme.py

### Pre-requisites

1.	input.def must be part of the package
2.	If config folder exists (.git>config) modify to include user details

```
[core]
	repositoryformatversion = 0
	filemode = true
	bare = false
	logallrefupdates = true
	ignorecase = true
	precomposeunicode = true
[remote "origin"]
	url = https://git.geomar.de/NEMO/NEMOGCM.git
	fetch = +refs/heads/*:refs/remotes/origin/*
[branch "release-3.6.3.x"]
	remote = origin
	merge = refs/heads/release-3.6.3.x
[user]
	name = <enter your name>
	email = <enter your email>
```


### Limitations

The current mkreadme script can be executed from a Nemo v3 and Nemo v4. However, the section reflecting the namelist_cfg has different parameters between the two version and they do not correspond. This has also been mentioned as an issue in this repository. 

### Build

    Load any python editor (This script was built by Anaconda Sypder)

    run mkReadme_V10.py


### Modules to install prior to executing the script

    pip install svn
    pip install wget
    pip install gitpython

The other modules listed in the script should be pre-installed with Anaconda. 


## Resources (Documentation and other links)
